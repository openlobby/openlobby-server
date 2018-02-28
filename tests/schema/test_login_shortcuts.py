import pytest

from openlobby.core.models import OpenIdClient

from ..utils import call_api


pytestmark = pytest.mark.django_db


def test_returns_only_shortcuts(client, snapshot):
    OpenIdClient.objects.create(id=10, name='foo', issuer='foo')
    OpenIdClient.objects.create(id=20, name='bar', issuer='bar', is_shortcut=True)
    query = """
    query {
        loginShortcuts {
            id
            name
        }
    }
    """
    response = call_api(client, query)
    snapshot.assert_match(response)


def test_none(client, snapshot):
    OpenIdClient.objects.create(id=10, name='foo')
    query = """
    query {
        loginShortcuts {
            id
            name
        }
    }
    """
    response = call_api(client, query)
    snapshot.assert_match(response)
