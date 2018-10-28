import pytest

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
