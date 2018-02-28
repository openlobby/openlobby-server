from graphql_relay import to_global_id
import pytest

from openlobby.core.models import OpenIdClient, LoginAttempt
from openlobby.core.openid import register_client

from .test_login import check_authorization_url
from ..utils import call_api

pytestmark = pytest.mark.django_db


def test_login_by_shortcut(issuer, client, snapshot):
    oc = register_client(issuer)
    oid_client = OpenIdClient.objects.create(name='Test', is_shortcut=True,
        issuer=issuer, client_id=oc.client_id, client_secret=oc.client_secret)

    app_redirect_uri = 'http://i.am.pirate'
    query = """
    mutation {{
        loginByShortcut (input: {{ shortcutId: "{id}", redirectUri: "{uri}" }}) {{
            authorizationUrl
        }}
    }}
    """.format(id=to_global_id('LoginShortcut', oid_client.id), uri=app_redirect_uri)
    response = call_api(client, query)

    assert 'errors' not in response
    authorization_url = response['data']['loginByShortcut']['authorizationUrl']

    la = LoginAttempt.objects.get(openid_client__id=oid_client.id)
    assert la.app_redirect_uri == app_redirect_uri
    assert la.openid_uid is None

    check_authorization_url(authorization_url, oid_client, la.state, snapshot)
