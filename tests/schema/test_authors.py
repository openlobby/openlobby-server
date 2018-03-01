import pytest

from openlobby.core.models import User

from ..dummy import prepare_reports
from ..utils import call_api


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures('django_es')]


def test_all(client, snapshot):
    prepare_reports()
    User.objects.create(id=4, is_author=False, username='x')
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
    response = call_api(client, query)
    snapshot.assert_match(response)


def test_first(client, snapshot):
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
    response = call_api(client, query)
    snapshot.assert_match(response)


def test_first_after(client, snapshot):
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
    response = call_api(client, query)
    snapshot.assert_match(response)


def test_last(client, snapshot):
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
    response = call_api(client, query)
    snapshot.assert_match(response)


def test_last_before(client, snapshot):
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
    response = call_api(client, query)
    snapshot.assert_match(response)


def test_with_reports(client, snapshot):
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
                            }
                        }
                    }
                }
            }
        }
    }
    """
    response = call_api(client, query)
    snapshot.assert_match(response)
