import pytest
import json
from unittest.mock import Mock

from openlobby.core.auth import create_access_token
from openlobby.core.middleware import TokenAuthMiddleware
from openlobby.core.models import User


pytestmark = pytest.mark.django_db


def test_no_auth_header():
    request = Mock()
    request.user = None
    request.META.get.return_value = None

    middleware = TokenAuthMiddleware(lambda r: r)
    response = middleware(request)

    request.META.get.assert_called_once_with('HTTP_AUTHORIZATION')
    assert response == request
    assert response.user is None


def test_authorized_user():
    user = User.objects.create(username='wolfe', first_name='Winston',
        last_name='Wolfe', email='winston@wolfe.com')
    request = Mock()
    request.user = None
    request.META.get.return_value = 'Bearer {}'.format(create_access_token('wolfe'))

    middleware = TokenAuthMiddleware(lambda r: r)
    response = middleware(request)

    request.META.get.assert_called_once_with('HTTP_AUTHORIZATION')
    assert response == request
    assert response.user == user


def test_wrong_header(snapshot):
    request = Mock()
    request.user = None
    request.META.get.return_value = 'WRONG {}'.format(create_access_token('unknown'))

    middleware = TokenAuthMiddleware(lambda r: r)
    response = middleware(request)

    request.META.get.assert_called_once_with('HTTP_AUTHORIZATION')
    assert response.status_code == 400
    snapshot.assert_match(json.loads(response.content))


def test_invalid_token(snapshot):
    request = Mock()
    request.user = None
    request.META.get.return_value = 'Bearer XXX{}'.format(create_access_token('unknown'))

    middleware = TokenAuthMiddleware(lambda r: r)
    response = middleware(request)

    request.META.get.assert_called_once_with('HTTP_AUTHORIZATION')
    assert response.status_code == 401
    snapshot.assert_match(json.loads(response.content))


def test_unknown_user(snapshot):
    request = Mock()
    request.user = None
    request.META.get.return_value = 'Bearer {}'.format(create_access_token('unknown'))

    middleware = TokenAuthMiddleware(lambda r: r)
    response = middleware(request)

    request.META.get.assert_called_once_with('HTTP_AUTHORIZATION')
    assert response == request
    assert response.user is None
