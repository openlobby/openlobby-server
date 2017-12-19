import pytest

from ..models import OpenIdClient


@pytest.mark.django_db
def test_login_shortcuts(client, snapshot):
    OpenIdClient.objects.create(id=10, name='foo')
    OpenIdClient.objects.create(id=20, name='bar', is_shortcut=True)
    res = client.post('/graphql', {'query': """
    query {
        loginShortcuts {
            id
            name
        }
    }
    """})
    snapshot.assert_match(res.content)


@pytest.mark.django_db
def test_login_shortcuts__none(client, snapshot):
    OpenIdClient.objects.create(id=10, name='foo')
    res = client.post('/graphql', {'query': """
    query {
        loginShortcuts {
            id
            name
        }
    }
    """})
    snapshot.assert_match(res.content)
