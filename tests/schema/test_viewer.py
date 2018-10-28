import pytest

from openlobby.core.auth import create_access_token


pytestmark = pytest.mark.django_db


def test_unauthenticated(call_api, snapshot, author_fix):
    query = """
    query {
        viewer {
            id
        }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_authenticated(call_api, snapshot, author_fix):
    query = """
    query {
        viewer {
            id
            firstName
            lastName
            hasCollidingName
            email
            openidUid
            isAuthor
            extra
        }
    }
    """
    response = call_api(query, user=author_fix)
    snapshot.assert_match(response)


# integration tests of wrong authentication


def test_wrong_header(client, snapshot, author_fix):
    token = create_access_token(author_fix.username)
    auth_header = "WRONG {}".format(token)
    res = client.post(
        "/graphql",
        {
            "query": """
    query {
        viewer {
            id
        }
    }
    """
        },
        HTTP_AUTHORIZATION=auth_header,
    )
    snapshot.assert_match(res.json())


def test_wrong_token(client, snapshot, author_fix):
    token = create_access_token(author_fix.username)
    auth_header = "Bearer XXX{}".format(token)
    res = client.post(
        "/graphql",
        {
            "query": """
    query {
        viewer {
            id
        }
    }
    """
        },
        HTTP_AUTHORIZATION=auth_header,
    )
    snapshot.assert_match(res.json())


def test_unknown_user(client, snapshot):
    token = create_access_token("unknown")
    auth_header = "Bearer {}".format(token)
    res = client.post(
        "/graphql",
        {
            "query": """
    query {
        viewer {
            id
        }
    }
    """
        },
        HTTP_AUTHORIZATION=auth_header,
    )
    snapshot.assert_match(res.json())
