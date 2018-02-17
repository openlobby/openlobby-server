from django.conf import settings
import jwt
import time


def create_access_token(username, expiration=None):
    if expiration is None:
        expiration = int(time.time() + settings.SESSION_EXPIRATION)
    payload = {
        'sub': username,
        'exp': expiration,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token.decode('utf-8')


def parse_access_token(token):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    return payload['sub']
