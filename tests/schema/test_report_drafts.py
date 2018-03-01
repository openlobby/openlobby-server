import pytest

from ..dummy import prepare_reports
from ..utils import call_api


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures('django_es')]


def test_unauthenticated(client, snapshot):
    prepare_reports()
    query = """
    query {
        reportDrafts {
            id
        }
    }
    """
    response = call_api(client, query)
    snapshot.assert_match(response)


def test_authenticated(client, snapshot):
    prepare_reports()
    query = """
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
            isDraft
        }
    }
    """
    response = call_api(client, query, username='wolf')
    snapshot.assert_match(response)
