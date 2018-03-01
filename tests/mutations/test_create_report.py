import pytest
import arrow
import re

from openlobby.core.models import Report

from ..dummy import prepare_author
from ..utils import call_api, strip_value


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures('django_es')]


query = """
mutation createReport ($input: CreateReportInput!) {
    createReport (input: $input) {
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
            isDraft
            extra
            author {
                id
                firstName
                lastName
                totalReports
                extra
            }
        }
    }
}
"""


@pytest.fixture(autouse=True)
def setup():
    prepare_author()


def test_unauthorized(client, snapshot):
    input = {
        'title': 'Short Story',
        'body': 'I told you!',
        'date': arrow.utcnow().isoformat(),
    }
    response = call_api(client, query, input)
    snapshot.assert_match(response)


def test_full_report(client, snapshot):
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

    response = call_api(client, query, input, 'wolf')

    published = strip_value(response, 'data', 'createReport', 'report', 'published')

    id = strip_value(response, 'data', 'createReport', 'report', 'id')
    assert re.match(r'\w+', id)

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
    assert report.is_draft is False


def test_input_sanitization(client):
    input = {
        'title': '<s>No</s> tags',
        'body': 'some <a href="http://foo">link</a> <br>in body',
        'receivedBenefit': '<b>coffee</b>',
        'providedBenefit': '<li>tea',
        'ourParticipants': 'me, <u>myself</u>',
        'otherParticipants': '<strong>you!</strong>',
        'date': arrow.utcnow().isoformat(),
    }

    call_api(client, query, input, 'wolf')

    report = Report.objects.get()
    assert report.title == 'No tags'
    assert report.body == 'some link in body'
    assert report.received_benefit == 'coffee'
    assert report.provided_benefit == 'tea'
    assert report.our_participants == 'me, myself'
    assert report.other_participants == 'you!'


def test_is_draft(client, snapshot):
    date = arrow.get(2018, 1, 3)
    title = 'Visited by old friend'
    body = 'Niel deGrasse Tyson just visited me...'
    received_benefit = 'touch of the God'
    provided_benefit = 'coffee'
    our_participants = 'myself'
    other_participants = 'Neil deGrasse Tyson'
    input = {
        'title': title,
        'body': body,
        'receivedBenefit': received_benefit,
        'providedBenefit': provided_benefit,
        'ourParticipants': our_participants,
        'otherParticipants': other_participants,
        'date': date.isoformat(),
        'isDraft': True,
    }

    response = call_api(client, query, input, 'wolf')

    published = strip_value(response, 'data', 'createReport', 'report', 'published')

    id = strip_value(response, 'data', 'createReport', 'report', 'id')
    assert re.match(r'\w+', id)

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
    assert report.is_draft is True
