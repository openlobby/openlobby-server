import pytest

from openlobby.core.models import User


pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def setup():
    User.objects.create(id=1, is_author=True, username='a', openid_uid='first',
        first_name='Winston', last_name='Wolfe', extra={'x': 1})
    User.objects.create(id=2, is_author=False, username='b')
    User.objects.create(id=3, is_author=True, username='c', openid_uid='second',
        first_name='Captain', last_name='Obvious')
    User.objects.create(id=4, is_author=True, username='d', openid_uid='third',
        first_name='Shaun', last_name='Sheep')
    yield


def test_all(client, snapshot):
    res = client.post('/graphql', {'query': """
    query {
        authors {
            totalCount
            edges {
                cursor
                node {
                    id
                    firstName
                    lastName
                    openidUid
                    extra
                }
            }
            pageInfo {
                hasPreviousPage
                hasNextPage
                startCursor
                endCursor
            }
        }
    }
    """})
    snapshot.assert_match(res.json())


def test_first(client, snapshot):
    res = client.post('/graphql', {'query': """
    query {
        authors (first: 2) {
            totalCount
            edges {
                cursor
                node {
                    openidUid
                }
            }
            pageInfo {
                hasPreviousPage
                hasNextPage
                startCursor
                endCursor
            }
        }
    }
    """})
    snapshot.assert_match(res.json())


def test_first_after(client, snapshot):
    res = client.post('/graphql', {'query': """
    query {
        authors (first: 1, after: "MQ==") {
            totalCount
            edges {
                cursor
                node {
                    openidUid
                }
            }
            pageInfo {
                hasPreviousPage
                hasNextPage
                startCursor
                endCursor
            }
        }
    }
    """})
    snapshot.assert_match(res.json())


def test_last(client, snapshot):
    res = client.post('/graphql', {'query': """
    query {
        authors (last: 2) {
            totalCount
            edges {
                cursor
                node {
                    openidUid
                }
            }
            pageInfo {
                hasPreviousPage
                hasNextPage
                startCursor
                endCursor
            }
        }
    }
    """})
    snapshot.assert_match(res.json())


def test_last_before(client, snapshot):
    res = client.post('/graphql', {'query': """
    query {
        authors (last: 1, before: "Mw==") {
            totalCount
            edges {
                cursor
                node {
                    openidUid
                }
            }
            pageInfo {
                hasPreviousPage
                hasNextPage
                startCursor
                endCursor
            }
        }
    }
    """})
    snapshot.assert_match(res.json())
