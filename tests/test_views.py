import pytest
from django.urls import reverse
from unittest.mock import patch
import urllib.parse

from openlobby.core.auth import parse_access_token
from openlobby.core.models import User, OpenIdClient, LoginAttempt
from openlobby.core.openid import register_client


pytestmark = pytest.mark.django_db


def test_login_redirect__new_user(client, issuer):
    state = 'IDDQD'
    sub = 'IDKFA'
    openid_uid = 'elon.musk@openid'
    first_name = 'Elon'
    last_name = 'Musk'
    email = 'elon.musk@tesla.com'
    app_redirect_uri = 'http://doom.is.legend'

    oc = register_client(issuer)
    oid_client = OpenIdClient.objects.create(name='Test', issuer=issuer,
        client_id=oc.client_id, client_secret=oc.client_secret)
    LoginAttempt.objects.create(openid_client=oid_client, state=state,
        app_redirect_uri=app_redirect_uri, openid_uid=openid_uid)

    # we are not testing real redirect url params, so we mock communication with
    # OpenID Provider
    user_info = {
        'sub': sub,
        'given_name': first_name,
        'family_name': last_name,
        'email': email,
    }
    with patch('openlobby.core.views.get_user_info', return_value=user_info) as mock:
        response = client.get(reverse('login-redirect'), {'state': state})
        m_client, m_query_string = mock.call_args[0]
        assert m_client.client_id == oc.client_id
        assert m_query_string == 'state={}'.format(state)

    assert response.status_code == 302
    url, query_string = response.url.split('?')
    qs = urllib.parse.parse_qs(query_string)
    assert url == app_redirect_uri
    assert sub == parse_access_token(qs['token'][0])

    user = User.objects.get()
    assert user.username == sub
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.email == email
    assert user.openid_uid == openid_uid


def test_login_redirect__existing_user(client, issuer):
    state = 'IDDQD'
    sub = 'IDKFA'
    openid_uid = 'elon.musk@openid'
    first_name = 'Elon'
    last_name = 'Musk'
    email = 'elon.musk@tesla.com'
    app_redirect_uri = 'http://doom.is.legend'

    oc = register_client(issuer)
    oid_client = OpenIdClient.objects.create(name='Test', issuer=issuer,
        client_id=oc.client_id, client_secret=oc.client_secret)
    LoginAttempt.objects.create(openid_client=oid_client, state=state,
        app_redirect_uri=app_redirect_uri, openid_uid=openid_uid)
    User.objects.create(username=sub, first_name=first_name, last_name=last_name,
        email=email, openid_uid=openid_uid)

    # we are not testing real redirect url params, so we mock communication with
    # OpenID Provider
    user_info = {
        'sub': sub,
        # return different details
        'given_name': 'Elons',
        'family_name': 'Mustache',
        'email': 'elons.mustache@spacex.com',
    }
    with patch('openlobby.core.views.get_user_info', return_value=user_info) as mock:
        response = client.get(reverse('login-redirect'), {'state': state})
        m_client, m_query_string = mock.call_args[0]
        assert m_client.client_id == oc.client_id
        assert m_query_string == 'state={}'.format(state)

    assert response.status_code == 302
    url, query_string = response.url.split('?')
    qs = urllib.parse.parse_qs(query_string)
    assert url == app_redirect_uri
    assert sub == parse_access_token(qs['token'][0])

    # check there is still just one user, who's details are not updated
    user = User.objects.get()
    assert user.username == sub
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.email == email
    assert user.openid_uid == openid_uid
