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

            authentication_required = getattr(handler(), 'authentication_required', False)
            if authentication_required:
                token_validated = self.validate_token(request, response)
                if not token_validated:
                    return response

            handler(request, response, **kwargs)
        else:
            self.not_found(response)

        return response


response = {
            "headers": {
                "Content-Type": "application/json"
            },
        }

request = {'resource': '/{proxy+}', 'path': '/login', 'httpMethod': 'POST', 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Authorization': 'Bearer eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..VZCo32kifjy2Xz5Sm8p1IQ.8oZrCRntW9fm-XhpWcY3EJdryGml9rlnVG1ia-ZrFPL0ruAkuXT2l7WHXWRdUgYTTRqk1P1TNx_NQw4sh1b6xPU01gl33-3AfJMIZQWyJMByxuynjARZElyfQ7uRCeUXbNQDSnPuG_g8Q7M8SejII9_mOoqAdBOrRUt3tZeszWovKQPz5fZaZN3RoQGlNhh0f7Rtxn4EM4yXpOdqx8IkldvAbYdBoRlkOlrp04_D1bSTyv6tkrqxpSNDie4Et_uMzJ4Q1z24ab8wSAjAGxPGwDNPx-Cq6rNTcjWmB_iqyzqlf1F3wjRXD38pCJTyIvszhDwORYR9GcZx29ptYOb7Ius6DDwCl274k1D5tB9d4J2f-pvmI94OZZf5wXuu9r5MM6sQurU38L9EmNWeggmV5YtWjdLwkANXkTllDCwjamVF2B-eTwnBAZtnNJD1mFaTDs_yQsOotvdN4B2QVYhTg1QSkJdgD08pVxf25Ah805k4zTY4JdHaPcqAlej_iM_FZqadPLtTC2m0DHq2UJLQ-PCnmOLQlAHdnA1-7rADm0eOAwijVWakxs49eM-CK1jZorom0NR1fJQle5Qgq_MNR_Ik2zaTSlLVTZNqTD5V17RHxL9nNQEilVuzAvIhGsoThzxv8PvirYwuLjwT5yWwfC8aAEit-YPvSEYHjJkLklJR6myeICSNaFMgDowhj0WHLA1lbRgGx-JTzEc_xILmHbisJoMZaYqkkmh-rJnZdrOsiB_E8yzascKWj44MdWKB.B2aZR2bzvpLfYRCJcuuhlw', 'CloudFront-Forwarded-Proto': 'https', 'CloudFront-Is-Desktop-Viewer': 'true', 'CloudFront-Is-Mobile-Viewer': 'false', 'CloudFront-Is-SmartTV-Viewer': 'false', 'CloudFront-Is-Tablet-Viewer': 'false', 'CloudFront-Viewer-ASN': '45899', 'CloudFront-Viewer-Country': 'VN', 'Content-Type': 'application/json', 'Host': 'q1s0nz03gj.execute-api.us-east-1.amazonaws.com', 'Postman-Token': '484c4c4c-a3b5-4b67-8794-747c80c8ad57', 'User-Agent': 'PostmanRuntime/7.29.2', 'Via': '1.1 3f0bb28fb1a9d7cc350db3a326fdc824.cloudfront.net (CloudFront)', 'X-Amz-Cf-Id': 'Y_xMwLXDP1JpBGxNhJI6WldZ77UXCMFtxUyXHsPrdsR9gEyEdmDFPQ==', 'X-Amzn-Trace-Id': 'Root=1-637c7fc9-6cf7e6970461fe2c0160b66c', 'X-Forwarded-For': '14.162.134.3, 15.158.12.36', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}, 'multiValueHeaders': {'Accept': ['*/*'], 'Accept-Encoding': ['gzip, deflate, br'], 'Authorization': ['Bearer eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..VZCo32kifjy2Xz5Sm8p1IQ.8oZrCRntW9fm-XhpWcY3EJdryGml9rlnVG1ia-ZrFPL0ruAkuXT2l7WHXWRdUgYTTRqk1P1TNx_NQw4sh1b6xPU01gl33-3AfJMIZQWyJMByxuynjARZElyfQ7uRCeUXbNQDSnPuG_g8Q7M8SejII9_mOoqAdBOrRUt3tZeszWovKQPz5fZaZN3RoQGlNhh0f7Rtxn4EM4yXpOdqx8IkldvAbYdBoRlkOlrp04_D1bSTyv6tkrqxpSNDie4Et_uMzJ4Q1z24ab8wSAjAGxPGwDNPx-Cq6rNTcjWmB_iqyzqlf1F3wjRXD38pCJTyIvszhDwORYR9GcZx29ptYOb7Ius6DDwCl274k1D5tB9d4J2f-pvmI94OZZf5wXuu9r5MM6sQurU38L9EmNWeggmV5YtWjdLwkANXkTllDCwjamVF2B-eTwnBAZtnNJD1mFaTDs_yQsOotvdN4B2QVYhTg1QSkJdgD08pVxf25Ah805k4zTY4JdHaPcqAlej_iM_FZqadPLtTC2m0DHq2UJLQ-PCnmOLQlAHdnA1-7rADm0eOAwijVWakxs49eM-CK1jZorom0NR1fJQle5Qgq_MNR_Ik2zaTSlLVTZNqTD5V17RHxL9nNQEilVuzAvIhGsoThzxv8PvirYwuLjwT5yWwfC8aAEit-YPvSEYHjJkLklJR6myeICSNaFMgDowhj0WHLA1lbRgGx-JTzEc_xILmHbisJoMZaYqkkmh-rJnZdrOsiB_E8yzascKWj44MdWKB.B2aZR2bzvpLfYRCJcuuhlw'], 'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'], 'CloudFront-Is-Mobile-Viewer': ['false'], 'CloudFront-Is-SmartTV-Viewer': ['false'], 'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-ASN': ['45899'], 'CloudFront-Viewer-Country': ['VN'], 'Content-Type': ['application/json'], 'Host': ['q1s0nz03gj.execute-api.us-east-1.amazonaws.com'], 'Postman-Token': ['484c4c4c-a3b5-4b67-8794-747c80c8ad57'], 'User-Agent': ['PostmanRuntime/7.29.2'], 'Via': ['1.1 3f0bb28fb1a9d7cc350db3a326fdc824.cloudfront.net (CloudFront)'], 'X-Amz-Cf-Id': ['Y_xMwLXDP1JpBGxNhJI6WldZ77UXCMFtxUyXHsPrdsR9gEyEdmDFPQ=='], 'X-Amzn-Trace-Id': ['Root=1-637c7fc9-6cf7e6970461fe2c0160b66c'], 'X-Forwarded-For': ['14.162.134.3, 15.158.12.36'], 'X-Forwarded-Port': ['443'], 'X-Forwarded-Proto': ['https']}, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': {'proxy': 'login'}, 'stageVariables': None, 'requestContext': {'resourceId': 'crodlx', 'resourcePath': '/{proxy+}', 'httpMethod': 'POST', 'extendedRequestId': 'b_jnjHk5oAMFryQ=', 'requestTime': '22/Nov/2022:07:52:41 +0000', 'path': '/prod/login', 'accountId': '611642177764', 'protocol': 'HTTP/1.1', 'stage': 'prod', 'domainPrefix': 'q1s0nz03gj', 'requestTimeEpoch': 1669103561762, 'requestId': 'c7b352d4-3087-4c08-847b-a938d906d08f', 'identity': {'cognitoIdentityPoolId': None, 'accountId': None, 'cognitoIdentityId': None, 'caller': None, 'sourceIp': '14.162.134.3', 'principalOrgId': None, 'accessKey': None, 'cognitoAuthenticationType': None, 'cognitoAuthenticationProvider': None, 'userArn': None, 'userAgent': 'PostmanRuntime/7.29.2', 'user': None}, 'domainName': 'q1s0nz03gj.execute-api.us-east-1.amazonaws.com', 'apiId': 'q1s0nz03gj'}, 'body': '{\n    "email": "test1@gmail.com",\n    "password": "123456"\n}', 'isBase64Encoded': False}


engine = create_engine(
    "postgresql://postgres:$lhA$*4F97$Z15Aydn5P@grocom-test.c0eqwkjkgcox.us-east-1.rds.amazonaws.com:5432/postgres")

api = API(engine=engine)
api.validate_token(request, response)