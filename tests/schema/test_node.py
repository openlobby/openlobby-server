import pytest
from graphql_relay import to_global_id

from openlobby.core.models import OpenIdClient, User

from ..dummy import prepare_reports


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("django_es")]


def test_login_shortcut(call_api, snapshot):
    OpenIdClient.objects.create(id=10, name="foo", issuer="foo", is_shortcut=True)
    query = """
    query {{
        node (id:"{id}") {{
            ... on LoginShortcut {{
                id
                name
            }}
        }}
    }}
    """.format(
        id=to_global_id("LoginShortcut", 10)
    )
    response = call_api(query)
    snapshot.assert_match(response)


def test_author(call_api, snapshot):
    prepare_reports()
    query = """
    query {{
        node (id:"{id}") {{
            ... on Author {{
                id
                firstName
                lastName
                hasCollidingName
                totalReports
                extra
            }}
        }}
    }}
    """.format(
        id=to_global_id("Author", 1)
    )
    response = call_api(query)
    snapshot.assert_match(response)


def test_author__returns_only_if_is_author(call_api, snapshot):
    User.objects.create(id=7, is_author=False)
    query = """
    query {{
        node (id:"{id}") {{
            ... on Author {{
                id
            }}
        }}
    }}
    """.format(
        id=to_global_id("Author", 7)
    )
    response = call_api(query)
    snapshot.assert_match(response)


def test_report(call_api, snapshot):
    prepare_reports()
    query = """
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
                isDraft
                extra
                edited
                author {{
                    id
                    firstName
                    lastName
                    hasCollidingName
                    totalReports
                    extra
                }}
            }}
        }}
    }}
    """.format(
        id=to_global_id("Report", 1)
    )
    response = call_api(query)
    snapshot.assert_match(response)


def test_report__is_draft(call_api, snapshot):
    prepare_reports()
    query = """
    query {{
        node (id:"{id}") {{
            ... on Report {{
                id
                title
                isDraft
            }}
        }}
    }}
    """.format(
        id=to_global_id("Report", 4)
    )
    response = call_api(query, user=User.objects.get(username="wolf"))
    snapshot.assert_match(response)


def test_report__is_draft__unauthorized_viewer(call_api, snapshot):
    prepare_reports()
    query = """
    query {{
        node (id:"{id}") {{
            ... on Report {{
                id
                title
                isDraft
            }}
        }}
    }}
    """.format(
        id=to_global_id("Report", 4)
    )
    response = call_api(query)
    snapshot.assert_match(response)


def test_report__is_draft__viewer_is_not_author(call_api, snapshot):
    prepare_reports()
    query = """
    query {{
        node (id:"{id}") {{
            ... on Report {{
                id
                title
                isDraft
            }}
        }}
    }}
    """.format(
        id=to_global_id("Report", 4)
    )
    response = call_api(query, user=User.objects.get(username="sponge"))
    snapshot.assert_match(response)


def test_report__without_revisions(call_api, snapshot):
    prepare_reports()
    query = """
    query {{
        node (id:"{id}") {{
            ... on Report {{
                id
                title
                hasRevisions
                revisions {{
                    id
                }}
            }}
        }}
    }}
    """.format(
        id=to_global_id("Report", 3)
    )
    response = call_api(query)
    snapshot.assert_match(response)


def test_report__with_revisions(call_api, snapshot):
    prepare_reports()
    query = """
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
                isDraft
                extra
                edited
                hasRevisions
                revisions {{
                    id
                    date
                    published
                    title
                    body
                    receivedBenefit
                    providedBenefit
                    ourParticipants
                    otherParticipants
                    isDraft
                    extra
                    edited
                }}
            }}
        }}
    }}
    """.format(
        id=to_global_id("Report", 2)
    )
    response = call_api(query)
    snapshot.assert_match(response)


def test_user__unauthorized(call_api, snapshot):
    User.objects.create(
        id=8,
        username="albert",
        openid_uid="albert@einstein.id",
        first_name="Albert",
        last_name="Einstein",
        extra={"e": "mc2"},
    )
    query = """
    query {{
        node (id:"{id}") {{
            ... on User {{
                id
                firstName
                lastName
                hasCollidingName
                openidUid
                isAuthor
                extra
            }}
        }}
    }}
    """.format(
        id=to_global_id("User", 8)
    )
    response = call_api(query)
    snapshot.assert_match(response)


def test_user__not_a_viewer(call_api, snapshot):
    User.objects.create(
        id=8,
        username="albert",
        openid_uid="albert@einstein.id",
        first_name="Albert",
        last_name="Einstein",
        extra={"e": "mc2"},
    )
    user = User.objects.create(
        id=2,
        username="isaac",
        openid_uid="isaac@newton.id",
        first_name="Isaac",
        last_name="Newton",
        extra={"apple": "hit"},
    )
    query = """
    query {{
        node (id:"{id}") {{
            ... on User {{
                id
                firstName
                lastName
                hasCollidingName
                openidUid
                isAuthor
                extra
            }}
        }}
    }}
    """.format(
        id=to_global_id("User", 8)
    )
    response = call_api(query, user=user)
    snapshot.assert_match(response)


def test_user(call_api, snapshot):
    user = User.objects.create(
        id=8,
        username="albert",
        openid_uid="albert@einstein.id",
        first_name="Albert",
        last_name="Einstein",
        extra={"e": "mc2"},
    )
    query = """
    query {{
        node (id:"{id}") {{
            ... on User {{
                id
                firstName
                lastName
                hasCollidingName
                openidUid
                isAuthor
                extra
            }}
        }}
    }}
    """.format(
        id=to_global_id("User", 8)
    )
    response = call_api(query, user=user)
    snapshot.assert_match(response)
