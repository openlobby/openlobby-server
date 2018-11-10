import pytest
from graphql_relay import from_global_id

from ..dummy import prepare_reports


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("django_es")]


def test_all(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        searchReports {
            totalCount
            edges {
                cursor
                node {
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
                    author {
                        id
                        firstName
                        lastName
                        hasCollidingName
                        totalReports
                        extra
                    }
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_query(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        searchReports (query: "towers") {
            totalCount
            edges {
                cursor
                node {
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
                    author {
                        id
                        firstName
                        lastName
                        hasCollidingName
                        totalReports
                        extra
                    }
                }
            }
        }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_highlight(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        searchReports (query: "Ring", highlight: true) {
            totalCount
            edges {
                cursor
                node {
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
                    author {
                        id
                        firstName
                        lastName
                        hasCollidingName
                        totalReports
                        extra
                    }
                }
            }
        }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_first(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        searchReports (first: 1) {
            totalCount
            edges {
                cursor
                node {
                    id
                    title
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_first_after(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        searchReports (first: 1, after: "MQ==") {
            totalCount
            edges {
                cursor
                node {
                    id
                    title
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_last(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        searchReports (last: 2) {
            totalCount
            edges {
                cursor
                node {
                    id
                    title
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_last_before(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        searchReports (last: 1, before: "Mw==") {
            totalCount
            edges {
                cursor
                node {
                    id
                    title
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


@pytest.mark.parametrize(
    "params, expected_ids",
    [
        ("sort: PUBLISHED", [3, 2, 1]),
        ("sort: PUBLISHED, reversed: true", [1, 2, 3]),
        ("sort: DATE", [2, 3, 1]),
        ("sort: DATE, reversed: true", [1, 3, 2]),
        ("sort: RELEVANCE", [3, 2, 1]),
        ("sort: RELEVANCE, reversed: true", [3, 2, 1]),
        ('query: "ring", sort: RELEVANCE', [1, 3]),
        ('query: "ring", sort: RELEVANCE, reversed: true', [3, 1]),
    ],
)
def test_sort(params, expected_ids, call_api, snapshot):
    prepare_reports()
    query = f"""
    query {{
        searchReports ({params}) {{
            totalCount
            edges {{
                cursor
                node {{
                    id
                }}
            }}
        }}
    }}
    """
    response = call_api(query)
    ids = [edge["node"]["id"] for edge in response["data"]["searchReports"]["edges"]]
    ids = [int(id) for type, id in map(from_global_id, ids)]
    assert ids == expected_ids
