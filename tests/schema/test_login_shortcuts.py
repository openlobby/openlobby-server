import pytest

from openlobby.core.models import OpenIdClient


pytestmark = pytest.mark.django_db


def test_returns_only_shortcuts(client, snapshot):
    OpenIdClient.objects.create(id=10, name='foo', issuer='foo')
    OpenIdClient.objects.create(id=20, name='bar', issuer='bar', is_shortcut=True)
    res = client.post('/graphql', {'query': """
    query {
        loginShortcuts {
            id
            name
        }
    }
    """})
    snapshot.assert_match(res.json())


def test_none(client, snapshot):
    OpenIdClient.objects.create(id=10, name='foo')
    res = client.post('/graphql', {'query': """
    query {
        loginShortcuts {
            id
            name
        }
    }
    """})
    snapshot.assert_match(res.json())
