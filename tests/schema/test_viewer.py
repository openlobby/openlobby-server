import pytest

from openlobby.core.auth import create_access_token
from openlobby.core.models import User


pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def setup():
    User.objects.create(id=1, is_author=True, username='wolfe', openid_uid='TheWolf',
        first_name='Winston', last_name='Wolfe', email='winston@wolfe.com')


def test_unauthenticated(client, snapshot):
    res = client.post('/graphql', {'query': """
    query {
        viewer {
            id
        }
    }
    """})
    snapshot.assert_match(res.json())


def test_authenticated(client, snapshot):
    token = create_access_token('wolfe')
    auth_header = 'Bearer {}'.format(token)
    res = client.post('/graphql', {'query': """
    query {
        viewer {
            id
            firstName
            lastName
            email
            openidUid
        }
    }
    """}, HTTP_AUTHORIZATION=auth_header)
    snapshot.assert_match(res.json())


# integration tests of wrong authentication

def test_wrong_header(client, snapshot):
    token = create_access_token('wolfe')
    auth_header = 'WRONG {}'.format(token)
    res = client.post('/graphql', {'query': """
    query {
        viewer {
            id
        }
    }
    """}, HTTP_AUTHORIZATION=auth_header)
    snapshot.assert_match(res.json())


def test_wrong_token(client, snapshot):
    token = create_access_token('wolfe')
    auth_header = 'Bearer XXX{}'.format(token)
    res = client.post('/graphql', {'query': """
    query {
        viewer {
            id
        }
    }
    """}, HTTP_AUTHORIZATION=auth_header)
    snapshot.assert_match(res.json())


def test_unknown_user(client, snapshot):
    token = create_access_token('unknown')
    auth_header = 'Bearer {}'.format(token)
    res = client.post('/graphql', {'query': """
    query {
        viewer {
            id
        }
    }
    """}, HTTP_AUTHORIZATION=auth_header)
    snapshot.assert_match(res.json())
