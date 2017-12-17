from django.conf import settings
import json
import jwt
import re
import time
from flask import g, request
from flask_graphql import GraphQLView


def get_login_attempt_expiration_time():
    return int(time.time() + settings.LOGIN_ATTEMPT_EXPIRATION)


def get_session_expiration_time():
    return int(time.time() + settings.SESSION_EXPIRATION)


def create_access_token(session_id, expiration):
    payload = {
        'sub': session_id,
        'exp': expiration,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token.decode('utf-8')


def parse_access_token(token):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    return payload['sub']


def graphql_error_response(message, code=400):
    error = {'message': message}
    return json.dumps({'errors': [error]}), code, {'Content-Type': 'application/json'}


class AuthGraphQLView(GraphQLView):
    """
    GraphQLView which sets session_id into 'g' if authorization token is
    provided in Authorization header.
    """

    def dispatch_request(self):
        session_id = None
        auth_header = request.headers.get('Authorization')
        if auth_header is not None:
            m = re.match(r'Bearer (?P<token>.+)', auth_header)
            if m:
                token = m.group('token')
            else:
                return graphql_error_response('Wrong Authorization header. Expected: "Bearer <token>"')

            try:
                session_id = parse_access_token(token)
            except jwt.InvalidTokenError:
                session_id = None
            except Exception:
                return graphql_error_response('Wrong Authorization token.', 401)

        g.session_id = session_id
        return super(AuthGraphQLView, self).dispatch_request()
