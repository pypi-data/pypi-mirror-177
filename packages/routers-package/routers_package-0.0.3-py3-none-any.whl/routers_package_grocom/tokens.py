import datetime
from uuid import uuid4
from sqlalchemy.orm import Session

from .state import token_type_claim, jti_claim, user_id_field, user_id_claim
from .state import token_backend
from .models import BlacklistedToken


class Token:
    """
    A class which validates and wraps an existing JWT or can be used to build a
    new JWT.
    """
    token_type = None
    lifetime = None
    engine = None

    def __init__(self, token=None, engine=None, verify=True):
        """
        !!!! IMPORTANT !!!! MUST raise a TokenError with a user-facing error
        message if the given token is invalid, expired, or otherwise not safe
        to use.
        """
        if self.token_type is None or self.lifetime is None:
            raise Exception('Cannot create token with no type or lifetime')

        self.token = token
        self.current_time = datetime.datetime.utcnow()
        self.engine = engine

        # Set up token
        if token is not None:
            # Decode token
            try:
                self.payload = token_backend.decode(token, verify=verify)
            except Exception:
                raise Exception('Token is invalid or expired')

            if verify:
                self.verify()
        else:
            # New token.  Skip all the verification steps.
            self.payload = {token_type_claim: self.token_type}

            # Set "exp" claim with default value
            self.set_exp(from_time=self.current_time, lifetime=self.lifetime)

            # Set "jti" claim
            self.set_jti()

    def __repr__(self):
        return repr(self.payload)

    def __getitem__(self, key):
        return self.payload[key]

    def __setitem__(self, key, value):
        self.payload[key] = value

    def __delitem__(self, key):
        del self.payload[key]

    def __contains__(self, key):
        return key in self.payload

    def get(self, key, default=None):
        return self.payload.get(key, default)

    def __str__(self):
        """
        Signs and returns a token as a base64 encoded string.
        """

        return token_backend.encode(self.payload)

    def verify(self):
        """
        Performs additional validation steps which were not performed when this
        token was decoded.  This method is part of the "public" API to indicate
        the intention that it may be overridden in subclasses.
        """
        # According to RFC 7519, the "exp" claim is OPTIONAL
        # (https://tools.ietf.org/html/rfc7519#section-4.1.4).  As a more
        # correct behavior for authorization tokens, we require an "exp"
        # claim.  We don't want any zombie tokens walking around.
        self.check_exp()

        # Ensure token id is present
        if jti_claim not in self.payload:
            raise Exception('Token has no id')

        self.verify_token_type()

    def verify_token_type(self):
        """
        Ensures that the token type claim is present and has the correct value.
        """
        try:
            token_type = self.payload[token_type_claim]
        except KeyError:
            raise Exception('Token has no type')
            # raise TokenError(_('Token has no type'))

        if self.token_type != token_type:
            raise Exception('Token has wrong type')
            # raise TokenError(_('Token has wrong type'))

    def set_jti(self):
        """
        Populates the configured jti claim of a token with a string where there
        is a negligible probability that the same string will be chosen at a
        later time.

        See here:
        https://tools.ietf.org/html/rfc7519#section-4.1.7
        """
        self.payload[jti_claim] = uuid4().hex

    def set_exp(self, claim='exp', from_time=None, lifetime=None):
        """
        Updates the expiration time of a token.
        """
        if from_time is None:
            from_time = self.current_time

        if lifetime is None:
            lifetime = self.lifetime

        self.payload[claim] = from_time + lifetime

    def check_exp(self, claim='exp', current_time=None):
        """
        Checks whether a timestamp value in the given claim has passed (since
        the given datetime value in `current_time`).  Raises a TokenError with
        a user-facing error message if so.
        """
        if current_time is None:
            current_time = self.current_time

        try:
            claim_value = self.payload[claim]
        except KeyError:
            error = 'Token has no ' + claim + ' claim'
            raise Exception(error)
            # raise TokenError(format_lazy(_("Token has no '{}' claim"), claim))

        # claim_time = datetime_from_epoch(claim_value)
        claim_value = datetime.datetime.utcfromtimestamp(claim_value)
        if claim_value <= current_time:
            error = 'Token ' + claim + ' claim has expired'
            raise Exception(error)
            # raise TokenError(format_lazy(_("Token '{}' claim has expired"), claim))

    @classmethod
    def for_user(cls, user):
        """
        Returns an authorization token for the given user that will be provided
        after authenticating the user's credentials.
        """
        user_id = getattr(user, user_id_field)
        if not isinstance(user_id, int):
            user_id = str(user_id)

        token = cls()
        token[user_id_claim] = user_id

        return token


class BlacklistMixin:
    """
    If the `rest_framework_simplejwt.token_blacklist` app was configured to be
    used, tokens created from `BlacklistMixin` subclasses will insert
    themselves into an outstanding token list and also check for their
    membership in a token blacklist.
    """
    # engine = None

    def verify(self, *args, **kwargs):
        self.check_blacklist()

        super().verify(*args, **kwargs)

    def check_blacklist(self):
        """
        Checks if this token is present in the token blacklist.  Raises
        `TokenError` if so.
        """
        jti = self.payload[jti_claim]
        # existed = None

        with Session(self.engine) as session:
            existed = session.query(BlacklistedToken).filter_by(jti=jti).first()

        if existed is not None:
            raise Exception('Token is blacklisted')
            # raise TokenError(_('Token is blacklisted'))

    def blacklist(self):
        """
        Ensures this token is included in the outstanding token list and
        adds it to the blacklist.
        """
        jti = self.payload[jti_claim]
        user_id = self.payload[user_id_claim]

        with Session(self.engine) as session:
            user = BlacklistedToken(jti=jti, user_id=user_id)
            session.add(user)
            session.commit()

        return True


class SlidingToken(BlacklistMixin, Token):
    token_type = 'sliding'
    lifetime = datetime.timedelta(days=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def for_user(cls, user, lifetime=None):
        """
        Returns an authorization token for the given user that will be provided
        after authenticating the user's credentials.
        """
        user_id = getattr(user, user_id_field)
        if not isinstance(user_id, int):
            user_id = str(user_id)

        token = cls()
        if lifetime is not None:
            token.lifetime = lifetime
        token[user_id_claim] = user_id
        token.set_exp(
            'exp',
            from_time=token.current_time,
            lifetime=lifetime,
        )

        access_token = token_backend.encode(token.payload)
        return access_token


class RefreshToken(Token):
    token_type = 'refresh'
    lifetime = datetime.timedelta(weeks=1)
    no_copy_claims = (
        token_type_claim,
        'exp',

        # Both of these claims are included even though they may be the same.
        # It seems possible that a third party token might have a custom or
        # namespaced JTI claim as well as a default "jti" claim.  In that case,
        # we wouldn't want to copy either one.
        jti_claim,
        'jti',
    )

    @property
    def access_token(self):
        """
        Returns an access token created from this refresh token.  Copies all
        claims present in this refresh token to the new access token except
        those claims listed in the `no_copy_claims` attribute.
        """
        access = AccessToken()

        # Use instantiation time of refresh token as relative timestamp for
        # access token "exp" claim.  This ensures that both a refresh and
        # access token expire relative to the same time if they are created as
        # a pair.
        access.set_exp(from_time=self.current_time)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value

        return access


class AccessToken(Token):
    token_type = 'access'
    lifetime = datetime.timedelta(days=1)


