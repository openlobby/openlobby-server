import pytest

from openlobby.core.models import User

from ..dummy import prepare_reports


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("django_es")]


def test_all(call_api, snapshot):
    prepare_reports()
    User.objects.create(id=4, is_author=False, username="x")
    query = """
    query {
        authors {
            totalCount
            edges {
                cursor
                node {
                    id
                    firstName
                    lastName
                    hasCollidingName
                    totalReports
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_first(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        authors (first: 2) {
            totalCount
            edges {
                cursor
                node {
                    id
                    firstName
                    lastName
                    hasCollidingName
                    totalReports
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_first_after(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        authors (first: 1, after: "MQ==") {
            totalCount
            edges {
                cursor
                node {
                    id
                    firstName
                    lastName
                    hasCollidingName
                    totalReports
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_last(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        authors (last: 2) {
            totalCount
            edges {
                cursor
                node {
                    id
                    firstName
                    lastName
                    hasCollidingName
                    totalReports
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_last_before(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        authors (last: 1, before: "Mw==") {
            totalCount
            edges {
                cursor
                node {
                    id
                    firstName
                    lastName
                    hasCollidingName
                    totalReports
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_with_reports(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        authors {
            edges {
                node {
                    id
                    firstName
                    lastName
                    hasCollidingName
                    totalReports
                    extra
                    reports {
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
                            }
                        }
                    }
                }
            }
        }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_sort_by_last_name(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        authors(sort: LAST_NAME) {
            totalCount
            edges {
                cursor
                node {
                    id
                    firstName
                    lastName
                    hasCollidingName
                    totalReports
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_sort_by_last_name_reversed(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        authors(sort: LAST_NAME, reversed: true) {
            totalCount
            edges {
                cursor
                node {
                    id
                    firstName
                    lastName
                    hasCollidingName
                    totalReports
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_sort_by_total_reports(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        authors(sort: TOTAL_REPORTS, reversed: false) {
            totalCount
            edges {
                cursor
                node {
                    id
                    firstName
                    lastName
                    hasCollidingName
                    totalReports
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_sort_by_total_reports_reversed(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        authors(sort: TOTAL_REPORTS, reversed: true) {
            totalCount
            edges {
                cursor
                node {
                    id
                    firstName
                    lastName
                    hasCollidingName
                    totalReports
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
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_sort_by_default_reversed(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        authors(reversed: true) {
            totalCount
            edges {
                cursor
                node {
                    id
                    firstName
                    lastName
                    hasCollidingName
                    totalReports
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
    """
    response = call_api(query)
    snapshot.assert_match(response)
