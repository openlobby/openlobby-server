from django.conf import settings
import time
import jwt
import pytest

from ..auth import (
    get_login_attempt_expiration_time,
    get_session_expiration_time,
    create_access_token,
    parse_access_token,
)


def test_get_login_attempt_expiration_time():
    expiration = get_login_attempt_expiration_time()
    expected = int(time.time() + settings.LOGIN_ATTEMPT_EXPIRATION)
    assert expected <= expiration <= expected + 1


def test_get_session_expiration_time():
    expiration = get_session_expiration_time()
    expected = int(time.time() + settings.SESSION_EXPIRATION)
    assert expected <= expiration <= expected + 1


def test_create_access_token():
    session_id = 'idkfa'
    expiration = int(time.time() + 10)
    token = create_access_token(session_id, expiration)
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    assert isinstance(token, str)
    assert payload['sub'] == session_id
    assert payload['exp'] == expiration


def test_parse_access_token():
    session_id = 'iddqd'
    expiration = int(time.time() + 10)
    token = create_access_token(session_id, expiration)
    result = parse_access_token(token)
    assert result == session_id


def test_parse_access_token__expired():
    session_id = 'idfa'
    expiration = int(time.time() - 1)
    token = create_access_token(session_id, expiration)
    with pytest.raises(jwt.ExpiredSignatureError):
        parse_access_token(token)
