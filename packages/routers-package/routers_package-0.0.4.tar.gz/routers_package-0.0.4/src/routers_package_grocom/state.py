import os

from .backend import TokenBackend


# algorithm = os.getenv('ALGORITHM', None)
# secret_key = os.getenv('SECRET_KEY', None)
# verifying_key = os.getenv('VERIFYING_KEY', None)
# audience = os.getenv('AUDIENCE', None)
# issuer = os.getenv('ISSUER', None)
# token_type_claim = os.getenv('TOKEN_TYPE_CLAIM', None)
# jti_claim = os.getenv('JTI_CLAIM', None)
# user_id_field = os.getenv('USER_ID_FIELD', None)
# user_id_claim = os.getenv('USER_ID_CLAIM', None)
algorithm = 'HS256'
secret_key = '*JzATIIT5dF4*hrJULWp*Jr8iP8dk3io'
verifying_key = None
audience = None
issuer = None
token_type_claim = 'token_type'
jti_claim = 'jti'
user_id_field = 'id'
user_id_claim = 'user_id'

token_backend = TokenBackend(algorithm, secret_key, verifying_key, audience, issuer)