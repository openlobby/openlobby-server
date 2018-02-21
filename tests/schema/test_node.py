import pytest
from graphql_relay import to_global_id

from openlobby.core.auth import create_access_token
from openlobby.core.models import OpenIdClient, User

from ..dummy import prepare_report


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures('django_es')]


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
                nameCollisionId
                totalReports
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


def test_report(client, snapshot):
    prepare_report()
    res = client.post('/graphql', {'query': """
    query {{
        node (id:"{id}") {{
            ... on Report {{
                id
                date
                published
                title
                body
                receivedBenefit
                providedBenefit
                ourParticipants
                otherParticipants
                extra
                author {{
                    id
                    firstName
                    lastName
                    nameCollisionId
                    totalReports
                    extra
                }}
            }}
        }}
    }}
    """.format(id=to_global_id('Report', 1))})
    snapshot.assert_match(res.json())


def test_user__unauthorized(client, snapshot):
    User.objects.create(id=8, username='albert', openid_uid='albert@einstein.id',
        first_name='Albert', last_name='Einstein', extra={'e': 'mc2'})
    res = client.post('/graphql', {'query': """
    query {{
        node (id:"{id}") {{
            ... on User {{
                id
                firstName
                lastName
                nameCollisionId
                openidUid
                isAuthor
                extra
            }}
        }}
    }}
    """.format(id=to_global_id('User', 8))})
    snapshot.assert_match(res.json())


def test_user__not_a_viewer(client, snapshot):
    User.objects.create(id=8, username='albert', openid_uid='albert@einstein.id',
        first_name='Albert', last_name='Einstein', extra={'e': 'mc2'})
    User.objects.create(id=2, username='isaac', openid_uid='isaac@newton.id',
        first_name='Isaac', last_name='Newton', extra={'apple': 'hit'})
    auth_header = 'Bearer {}'.format(create_access_token('isaac'))
    res = client.post('/graphql', {'query': """
    query {{
        node (id:"{id}") {{
            ... on User {{
                id
                firstName
                lastName
                nameCollisionId
                openidUid
                isAuthor
                extra
            }}
        }}
    }}
    """.format(id=to_global_id('User', 8))}, HTTP_AUTHORIZATION=auth_header)
    snapshot.assert_match(res.json())


def test_user(client, snapshot):
    User.objects.create(id=8, username='albert', openid_uid='albert@einstein.id',
            first_name='Albert', last_name='Einstein', extra={'e': 'mc2'})
    auth_header = 'Bearer {}'.format(create_access_token('albert'))
    res = client.post('/graphql', {'query': """
    query {{
        node (id:"{id}") {{
            ... on User {{
                id
                firstName
                lastName
                nameCollisionId
                openidUid
                isAuthor
                extra
            }}
        }}
    }}
    """.format(id=to_global_id('User', 8))}, HTTP_AUTHORIZATION=auth_header)
    snapshot.assert_match(res.json())
