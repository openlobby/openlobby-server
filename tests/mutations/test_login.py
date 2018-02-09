from graphql_relay import to_global_id
import json
import pytest
from urllib.parse import urlparse, urlunparse, parse_qs
from unittest.mock import patch

from openlobby.core.models import OpenIdClient, LoginAttempt


pytestmark = pytest.mark.django_db


def _check_authorization_url(authorization_url, oid_client, state, snapshot):
    url = urlparse(authorization_url)
    url_without_query = urlunparse((url.scheme, url.netloc, url.path, '', '', ''))
    assert url_without_query == '{}/protocol/openid-connect/auth'.format(oid_client.issuer)

    qs = parse_qs(url.query)
    assert qs['client_id'][0] == oid_client.client_id
    assert qs['response_type'][0] == 'code'
    assert qs['scope'][0] == 'openid'
    assert qs['redirect_uri'][0] == 'http://localhost:8010/login-redirect'
    assert qs['state'][0] == state
    snapshot.assert_match(json.loads(qs['claims'][0]))


def test_login_by_shortcut(keycloak, client, snapshot):
    oid_client = OpenIdClient.objects.create(name='Test', is_shortcut=True, **keycloak)

    app_redirect_uri = 'http://i.am.pirate'
    res = client.post('/graphql', {'query': """
    mutation {{
        loginByShortcut (input: {{ shortcutId: "{id}", redirectUri: "{uri}" }}) {{
            authorizationUrl
        }}
    }}
    """.format(id=to_global_id('LoginShortcut', oid_client.id), uri=app_redirect_uri)})
    response = res.json()
    assert 'errors' not in response
    authorization_url = response['data']['loginByShortcut']['authorizationUrl']

    la = LoginAttempt.objects.get(openid_client__id=oid_client.id)
    assert la.app_redirect_uri == app_redirect_uri

    _check_authorization_url(authorization_url, oid_client, la.state, snapshot)


def test_login__known_openid_client(keycloak, client, snapshot):
    oid_client = OpenIdClient.objects.create(name='Test', **keycloak)

    app_redirect_uri = 'http://i.am.pirate'
    openid_uid = 'wolf@openid.provider'
    # Keycloak does not support issuer discovery by UID, so we mock it
    with patch('openlobby.core.api.mutations.discover_issuer', return_value=oid_client.issuer) as mock:
        res = client.post('/graphql', {'query': """
        mutation {{
            login (input: {{ openidUid: "{uid}", redirectUri: "{uri}" }}) {{
                authorizationUrl
            }}
        }}
        """.format(uid=openid_uid, uri=app_redirect_uri)})
        mock.assert_called_once_with(openid_uid)

    response = res.json()
    assert 'errors' not in response
    authorization_url = response['data']['login']['authorizationUrl']

    la = LoginAttempt.objects.get(openid_client__id=oid_client.id)
    assert la.app_redirect_uri == app_redirect_uri

    _check_authorization_url(authorization_url, oid_client, la.state, snapshot)
