import re

import inspect
import json

from sqlalchemy import create_engine

from .tokens import SlidingToken


class API:
    engine = None

    def __init__(self, engine=None):
        self.routes = {}
        self.engine = engine

    def route(self, path, handler):
        # assert path not in self.routes, "Such route already exists."
        self.routes[path] = handler

    def not_found(self, response):
        response['statusCode'] = 404
        response['body'] = json.dumps({
            "message": "Not found"
        })

    def method_not_allowed(self, response):
        response['statusCode'] = 405
        response['body'] = json.dumps({
            "message": "Method not allowed"
        })

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            re_path = re.compile(path)
            match = re_path.search(request_path)

            if match:
                kwargs = match.groupdict()
                return handler, kwargs

        return None, None

    def validate_token(self, request, response):
        headers = request.get('headers', None)

        if headers is None:
            response['statusCode'] = 400
            response['body'] = json.dumps({
                'code': 'missing_headers',
                'message': 'Missing headers'
            })
            return False

        bearer_token = headers.get('Authorization', None)

        if bearer_token is None:
            response['statusCode'] = 400
            response['body'] = json.dumps({
                'code': 'missing_bearer_token',
                'message': 'Missing bearer token'
            })
            return False

        bearer_token = bearer_token.split()

        try:
            sliding_token = SlidingToken(token=bearer_token[-1], engine=self.engine)
            sliding_token.verify()
            return True
        except Exception as ex:
            print(ex)
            response['statusCode'] = 401
            response['body'] = json.dumps({
                'code': 'unauthorized',
                'message': 'Unauthorized'
            })
            return False

    def handle_request(self, request):
        response = {
            "headers": {
                "Content-Type": "application/json"
            },
        }
        method = request.get('httpMethod', None)

        handler, kwargs = self.find_handler(request_path=request['path'])

        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), method.lower(), None)
                if handler is None:
                    self.method_not_allowed(response)
                    return response

            try:
                authentication_required = handler.authentication_required
                if authentication_required:
                    token_validated = self.validate_token(request, response)
                    if not token_validated:
                        return response
            except Exception as ex:
                print(ex)

            handler(request, response, **kwargs)
        else:
            self.not_found(response)

        return response
