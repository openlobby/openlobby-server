import pytest
from openlobby.core.api.schema import REPORT_SORT_DATE_ID
from openlobby.core.models import User, Report

from ..dummy import prepare_reports, search_reports_query, authors, reports
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


def test_all_sort_by_date(client, snapshot):
    prepare_reports()
    author4 = User.objects.create(**authors[3])
    Report.objects.create(author=author4, **reports[5])

    for query in search_reports_query(sort='DATE'):
        response = call_api(client, query)
        snapshot.assert_match(response)


def test_all_sort_by_published(client, snapshot):
    prepare_reports()
    author4 = User.objects.create(**authors[3])
    Report.objects.create(author=author4, **reports[5])

    for query in search_reports_query(sort='PUBLISHED'):
        response = call_api(client, query)
        snapshot.assert_match(response)


def test_all_sort_by_relevance(client, snapshot):
    prepare_reports()
    author4 = User.objects.create(**authors[3])
    Report.objects.create(author=author4, **reports[5])

    for query in search_reports_query(sort='RELEVANCE'):
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
