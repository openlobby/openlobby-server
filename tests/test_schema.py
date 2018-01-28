import pytest
from graphql_relay import to_global_id

from openlobby.core.models import OpenIdClient, User


@pytest.mark.django_db
def test_login_shortcuts(client, snapshot):
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
    snapshot.assert_match(res.json())


@pytest.mark.django_db
def test_node__login_shortcut(client, snapshot):
    OpenIdClient.objects.create(id=10, name='foo', issuer='foo', is_shortcut=True)
    res = client.post('/graphql', {'query': """
    query {{
        node (id:"{id}") {{
            ... on LoginShortcut {{
                id
                name
            }}
        }}
    }}
    """.format(id=to_global_id('LoginShortcut', 10))})
    snapshot.assert_match(res.json())


@pytest.mark.django_db
def test_node__author(client, snapshot):
    User.objects.create(
        id=5,
        is_author=True,
        openid_uid='TheWolf',
        first_name='Winston',
        last_name='Wolfe',
        extra={'x': 1},
    )
    res = client.post('/graphql', {'query': """
    query {{
        node (id:"{id}") {{
            ... on Author {{
                id
                firstName
                lastName
                openidUid
                extra
            }}
        }}
    }}
    """.format(id=to_global_id('Author', 5))})
    snapshot.assert_match(res.json())


@pytest.mark.django_db
def test_node__author__only_if_is_author(client, snapshot):
    User.objects.create(id=7, is_author=False)
    res = client.post('/graphql', {'query': """
    query {{
        node (id:"{id}") {{
            ... on Author {{
                id
            }}
        }}
    }}
    """.format(id=to_global_id('Author', 7))})
    snapshot.assert_match(res.json())


@pytest.mark.django_db
class TestAuthors:

    @pytest.fixture(autouse=True)
    def setup(self):
        User.objects.create(id=1, is_author=True, username='a', openid_uid='first',
            first_name='Winston', last_name='Wolfe', extra={'x': 1})
        User.objects.create(id=2, is_author=False, username='b')
        User.objects.create(id=3, is_author=True, username='c', openid_uid='second',
            first_name='Captain', last_name='Obvious')
        User.objects.create(id=4, is_author=True, username='d', openid_uid='third',
            first_name='Shaun', last_name='Sheep')
        yield

    def test_all(self, client, snapshot):
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

    def test_first(self, client, snapshot):
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

    def test_first_after(self, client, snapshot):
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

    def test_last(self, client, snapshot):
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

    def test_last_before(self, client, snapshot):
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
