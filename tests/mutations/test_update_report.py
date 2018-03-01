import pytest
import arrow
from graphql_relay import to_global_id
from unittest.mock import patch

from openlobby.core.models import User, Report

from ..dummy import prepare_report
from ..utils import call_api


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures('django_es')]


query = """
mutation updateReport ($input: UpdateReportInput!) {
    updateReport (input: $input) {
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

published = arrow.get(2018, 3, 8)

date = arrow.get(2018, 3, 3)
title = 'Free Tesla'
body = 'I visited Tesla factory and talked with Elon Musk.'
received_benefit = 'Tesla Model S'
provided_benefit = 'nothing'
our_participants = 'me'
other_participants = 'Elon Musk'


def get_input(is_draft=False, id=1):
    return {
        'id': to_global_id('Report', id),
        'title': title,
        'body': body,
        'receivedBenefit': received_benefit,
        'providedBenefit': provided_benefit,
        'ourParticipants': our_participants,
        'otherParticipants': other_participants,
        'date': date.isoformat(),
        'isDraft': is_draft,
    }


def assert_report(is_draft=False):
    report = Report.objects.get(id=1)
    assert report.author_id == 1
    assert report.date == date.datetime
    assert report.published == published.datetime
    assert report.title == title
    assert report.body == body
    assert report.received_benefit == received_benefit
    assert report.provided_benefit == provided_benefit
    assert report.our_participants == our_participants
    assert report.other_participants == other_participants
    assert report.extra is None
    assert report.is_draft is is_draft


def test_unauthorized(client, snapshot):
    prepare_report()
    input = get_input()
    response = call_api(client, query, input)
    snapshot.assert_match(response)


def test_not_author(client, snapshot):
    prepare_report()
    User.objects.create(id=2, username='hacker')
    input = get_input()
    response = call_api(client, query, input, 'hacker')
    snapshot.assert_match(response)


def test_report_does_not_exist(client, snapshot):
    prepare_report()
    input = get_input(id=666)
    response = call_api(client, query, input, 'wolf')
    snapshot.assert_match(response)


def test_update_published_with_draft(client, snapshot):
    prepare_report()
    input = get_input(is_draft=True)
    response = call_api(client, query, input, 'wolf')
    snapshot.assert_match(response)


def test_update_draft_with_draft(client, snapshot):
    prepare_report(is_draft=True)
    input = get_input(is_draft=True)
    with patch('openlobby.core.api.mutations.arrow.utcnow', return_value=published):
        response = call_api(client, query, input, 'wolf')
    snapshot.assert_match(response)
    assert_report(is_draft=True)


def test_update_draft_with_published(client, snapshot):
    prepare_report(is_draft=True)
    input = get_input()
    with patch('openlobby.core.api.mutations.arrow.utcnow', return_value=published):
        response = call_api(client, query, input, 'wolf')
    snapshot.assert_match(response)
    assert_report()


def test_update_published_with_published(client, snapshot):
    prepare_report()
    input = get_input()
    with patch('openlobby.core.api.mutations.arrow.utcnow', return_value=published):
        response = call_api(client, query, input, 'wolf')
    snapshot.assert_match(response)
    assert_report()


def test_input_sanitization(client, snapshot):
    prepare_report()
    input = {
        'id': to_global_id('Report', 1),
        'title': '<s>No</s> tags',
        'body': 'some <a href="http://foo">link</a> <br>in body',
        'receivedBenefit': '<b>coffee</b>',
        'providedBenefit': '<li>tea',
        'ourParticipants': 'me, <u>myself</u>',
        'otherParticipants': '<strong>you!</strong>',
        'date': date.isoformat(),
    }

    with patch('openlobby.core.api.mutations.arrow.utcnow', return_value=published):
        response = call_api(client, query, input, 'wolf')

    snapshot.assert_match(response)

    report = Report.objects.get()
    assert report.title == 'No tags'
    assert report.body == 'some link in body'
    assert report.received_benefit == 'coffee'
    assert report.provided_benefit == 'tea'
    assert report.our_participants == 'me, myself'
    assert report.other_participants == 'you!'
