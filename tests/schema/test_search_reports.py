import pytest

from ..dummy import prepare_reports
from ..utils import call_api


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures('django_es')]


def test_all(client, snapshot):
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
    response = call_api(client, query)
    snapshot.assert_match(response)


def test_query(client, snapshot):
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
    response = call_api(client, query)
    snapshot.assert_match(response)


def test_highlight(client, snapshot):
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
    response = call_api(client, query)
    snapshot.assert_match(response)


def test_first(client, snapshot):
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
    response = call_api(client, query)
    snapshot.assert_match(response)


def test_first_after(client, snapshot):
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
    response = call_api(client, query)
    snapshot.assert_match(response)


def test_last(client, snapshot):
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
    response = call_api(client, query)
    snapshot.assert_match(response)


def test_last_before(client, snapshot):
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
    response = call_api(client, query)
    snapshot.assert_match(response)
