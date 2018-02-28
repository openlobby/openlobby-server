import json
import pytest
import re
from urllib.parse import urlparse, urlunparse, parse_qs
from unittest.mock import patch

from openlobby.core.models import OpenIdClient, LoginAttempt
from openlobby.core.openid import register_client

from ..utils import call_api


pytestmark = pytest.mark.django_db


def check_authorization_url(authorization_url, oid_client, state, snapshot):
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


def test_login__known_openid_client(issuer, client, snapshot):
    oc = register_client(issuer)
    oid_client = OpenIdClient.objects.create(name='Test', issuer=issuer,
        client_id=oc.client_id, client_secret=oc.client_secret)

    app_redirect_uri = 'http://i.am.pirate'
    openid_uid = 'wolf@openid.provider'
    query = """
    mutation {{
        login (input: {{ openidUid: "{uid}", redirectUri: "{uri}" }}) {{
            authorizationUrl
        }}
    }}
    """.format(uid=openid_uid, uri=app_redirect_uri)
    # Keycloak server used for tests does not support issuer discovery by UID, so we mock it
    with patch('openlobby.core.api.mutations.discover_issuer', return_value=issuer) as mock:
        response = call_api(client, query)
        mock.assert_called_once_with(openid_uid)

    assert 'errors' not in response
    authorization_url = response['data']['login']['authorizationUrl']

    la = LoginAttempt.objects.get(openid_client__id=oid_client.id)
    assert la.app_redirect_uri == app_redirect_uri
    assert la.openid_uid == openid_uid

    check_authorization_url(authorization_url, oid_client, la.state, snapshot)


def test_login__new_openid_client(issuer, client, snapshot):
    app_redirect_uri = 'http://i.am.pirate'
    openid_uid = 'wolf@openid.provider'
    query = """
    mutation {{
        login (input: {{ openidUid: "{uid}", redirectUri: "{uri}" }}) {{
            authorizationUrl
        }}
    }}
    """.format(uid=openid_uid, uri=app_redirect_uri)
    # Keycloak server used for tests does not support issuer discovery by UID, so we mock it
    with patch('openlobby.core.api.mutations.discover_issuer', return_value=issuer) as mock:
        response = call_api(client, query)
        mock.assert_called_once_with(openid_uid)

    assert 'errors' not in response
    authorization_url = response['data']['login']['authorizationUrl']

    oid_client = OpenIdClient.objects.get()
    assert oid_client.name == issuer
    assert oid_client.issuer == issuer
    assert re.match(r'\w+', oid_client.client_id)
    assert re.match(r'\w+', oid_client.client_secret)

    la = LoginAttempt.objects.get(openid_client__id=oid_client.id)
    assert la.app_redirect_uri == app_redirect_uri
    assert la.openid_uid == openid_uid

    check_authorization_url(authorization_url, oid_client, la.state, snapshot)
