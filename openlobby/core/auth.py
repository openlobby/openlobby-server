from django.conf import settings
import json
import jwt
import time


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
