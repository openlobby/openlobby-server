import pytest
from django.urls import reverse
from unittest.mock import patch

from openlobby.core.models import User, OpenIdClient, LoginAttempt
from openlobby.core.openid import register_client


pytestmark = pytest.mark.django_db


def test_login_redirect(client, issuer):
    state = 'IDDQD'
    app_redirect_uri = 'http://doom.is.legend'
    oc = register_client(issuer)
    oid_client = OpenIdClient.objects.create(name='Test', issuer=issuer,
        client_id=oc.client_id, client_secret=oc.client_secret)
    LoginAttempt.objects.create(openid_client=oid_client, state=state,
        app_redirect_uri=app_redirect_uri)

    # we are not testing real redirect url params, so we mock communication with
    # OpenID Provider
    user_info = {
        'sub': 'IDKFA',
        'given_name': 'Elon',
        'family_name': 'Musk',
        'email': 'elon.musk@tesla.com',
    }
    with patch('openlobby.core.views.get_user_info', return_value=user_info) as mock:
        response = client.get(reverse('login-redirect'), {'state': state})
        m_client, m_query_string = mock.call_args[0]

    assert m_client.client_id == oc.client_id
    assert m_query_string == 'state={}'.format(state)
    assert response.status_code == 302
    assert response.url == app_redirect_uri

    # TODO
    """
    user = User.objects.get()
    assert user.openid_sub == 'IDKFA'
    assert user.first_name == 'Elon'
    assert user.last_name == 'Musk'
    assert user.email == 'elon.musk@tesla.com'
    """
