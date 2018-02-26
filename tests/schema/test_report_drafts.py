import pytest

from openlobby.core.auth import create_access_token

from ..dummy import prepare_reports


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures('django_es')]


def test_unauthenticated(client, snapshot):
    prepare_reports()
    res = client.post('/graphql', {'query': """
    query {
        reportDrafts {
            id
        }
    }
    """})
    snapshot.assert_match(res.json())


def test_authenticated(client, snapshot):
    prepare_reports()
    token = create_access_token('Wolf')
    auth_header = 'Bearer {}'.format(token)
    res = client.post('/graphql', {'query': """
    query {
        reportDrafts {
            id
            date
            published
            title
            body
            receivedBenefit
            providedBenefit
            ourParticipants
            otherParticipants
        }
    }
    """}, HTTP_AUTHORIZATION=auth_header)
    snapshot.assert_match(res.json())
