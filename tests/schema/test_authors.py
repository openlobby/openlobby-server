import pytest

from openlobby.core.models import User

from ..dummy import prepare_authors, prepare_report


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures('django_es')]


def test_all(client, snapshot):
    prepare_authors()
    User.objects.create(id=4, is_author=False, username='x')
    res = client.post('/graphql', {'query': """
    query {
        authors {
            totalCount
            edges {
                cursor
                node {
                    id
                    firstName
                    lastName
                    openidUid
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
    """})
    snapshot.assert_match(res.json())


def test_first(client, snapshot):
    prepare_authors()
    res = client.post('/graphql', {'query': """
    query {
        authors (first: 2) {
            totalCount
            edges {
                cursor
                node {
                    openidUid
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
    """})
    snapshot.assert_match(res.json())


def test_first_after(client, snapshot):
    prepare_authors()
    res = client.post('/graphql', {'query': """
    query {
        authors (first: 1, after: "MQ==") {
            totalCount
            edges {
                cursor
                node {
                    openidUid
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
    """})
    snapshot.assert_match(res.json())


def test_last(client, snapshot):
    prepare_authors()
    res = client.post('/graphql', {'query': """
    query {
        authors (last: 2) {
            totalCount
            edges {
                cursor
                node {
                    openidUid
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
    """})
    snapshot.assert_match(res.json())


def test_last_before(client, snapshot):
    prepare_authors()
    res = client.post('/graphql', {'query': """
    query {
        authors (last: 1, before: "Mw==") {
            totalCount
            edges {
                cursor
                node {
                    openidUid
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
    """})
    snapshot.assert_match(res.json())


def test_with_reports(client, snapshot):
    prepare_report()
    res = client.post('/graphql', {'query': """
    query {
        authors {
            edges {
                node {
                    id
                    firstName
                    lastName
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
                                extra
                            }
                        }
                    }
                }
            }
        }
    }
    """})
    snapshot.assert_match(res.json())
