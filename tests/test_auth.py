from django.conf import settings
import time
import jwt
import pytest

from openlobby.core.auth import create_access_token, parse_access_token


def test_create_access_token():
    username = "idkfa"
    token = create_access_token(username)
    payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )
    assert isinstance(token, str)
    assert payload["sub"] == username
    expected_expiration = int(time.time() + settings.SESSION_EXPIRATION)
    assert expected_expiration <= payload["exp"] <= expected_expiration + 1


def test_parse_access_token():
    username = "iddqd"
    token = create_access_token(username)
    result = parse_access_token(token)
    assert result == username


def test_parse_access_token__expired():
    username = "idfa"
    expiration = int(time.time() - 1)
    token = create_access_token(username, expiration)
    with pytest.raises(jwt.ExpiredSignatureError):
        parse_access_token(token)
