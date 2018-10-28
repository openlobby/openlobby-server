import pytest

from openlobby.core.models import User

from ..dummy import prepare_reports


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("django_es")]


def test_unauthenticated(call_api, snapshot):
    prepare_reports()
    query = """
    query {
        reportDrafts {
            id
        }
    }
    """
    response = call_api(query)
    snapshot.assert_match(response)


def test_authenticated(call_api, snapshot):
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
            edited
        }
    }
    """
    response = call_api(query, user=User.objects.get(username="wolf"))
    snapshot.assert_match(response)
