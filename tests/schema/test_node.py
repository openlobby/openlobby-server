import pytest
from graphql_relay import to_global_id

from openlobby.core.models import OpenIdClient, User


pytestmark = pytest.mark.django_db


def test_login_shortcut(client, snapshot):
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


def test_author(client, snapshot):
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


def test_author__returns_only_if_is_author(client, snapshot):
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
