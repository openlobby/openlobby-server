import pytest
import arrow
import json
from unittest.mock import patch

from openlobby.core.auth import create_access_token
from openlobby.core.models import User, Report


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures('django_es')]


@pytest.fixture(autouse=True)
def setup():
    User.objects.create(id=1, is_author=True, username='wolfe',
        first_name='Winston', last_name='Wolfe', email='winston@wolfe.com')


def call_api(client, query, input, username=None):
    variables = json.dumps({'input': input})
    if username is None:
        res = client.post('/graphql', {'query': query, 'variables': variables})
    else:
        token = create_access_token(username)
        auth_header = 'Bearer {}'.format(token)
        res = client.post('/graphql', {'query': query, 'variables': variables},
            HTTP_AUTHORIZATION=auth_header)
    return res.json()


def test_unauthorized(client, snapshot):
    query = """
    mutation newReport ($input: NewReportInput!) {
        newReport (input: $input) {
            report {
                id
            }
        }
    }
    """
    input = {
        'title': 'Short Story',
        'body': 'I told you!',
        'date': arrow.utcnow().isoformat(),
    }

    response = call_api(client, query, input)

    snapshot.assert_match(response)


def test_full_report(client, snapshot):
    query = """
    mutation newReport ($input: NewReportInput!) {
        newReport (input: $input) {
            report {
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
                author {
                    id
                    firstName
                    lastName
                    extra
                }
            }
        }
    }
    """
    date = arrow.get(2018, 1, 1)
    title = 'Free Tesla'
    body = 'I visited Tesla factory and talked with Elon Musk.'
    received_benefit = 'Tesla Model S'
    provided_benefit = 'nothing'
    our_participants = 'me'
    other_participants = 'Elon Musk'
    input = {
        'title': title,
        'body': body,
        'receivedBenefit': received_benefit,
        'providedBenefit': provided_benefit,
        'ourParticipants': our_participants,
        'otherParticipants': other_participants,
        'date': date.isoformat(),
    }

    response = call_api(client, query, input, 'wolfe')

    published = response['data']['newReport']['report']['published']
    response['data']['newReport']['report']['published'] = '__STRIPPED__'
    snapshot.assert_match(response)

    report = Report.objects.get()
    assert report.author_id == 1
    assert report.date == date.datetime
    assert report.published == arrow.get(published).datetime
    assert report.title == title
    assert report.body == body
    assert report.received_benefit == received_benefit
    assert report.provided_benefit == provided_benefit
    assert report.our_participants == our_participants
    assert report.other_participants == other_participants
    assert report.extra is None
