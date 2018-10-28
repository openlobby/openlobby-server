import pytest
import arrow
import re

from openlobby.core.models import Report

from ..utils import strip_value, dates_to_iso


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("django_es")]


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
            edited
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


def test_unauthorized(call_api, snapshot):
    input = {
        "title": "Short Story",
        "body": "I told you!",
        "date": arrow.utcnow().isoformat(),
    }
    response = call_api(query, input)
    snapshot.assert_match(response)


@pytest.mark.freeze_time("2018-01-01T01:02:03")
def test_full_report(call_api, snapshot, author_fix):
    date = arrow.get(2018, 1, 1)
    title = "Free Tesla"
    body = "I visited Tesla factory and talked with Elon Musk."
    received_benefit = "Tesla Model S"
    provided_benefit = "nothing"
    our_participants = "me"
    other_participants = "Elon Musk"
    input = {
        "title": title,
        "body": body,
        "receivedBenefit": received_benefit,
        "providedBenefit": provided_benefit,
        "ourParticipants": our_participants,
        "otherParticipants": other_participants,
        "date": date.isoformat(),
    }

    response = call_api(query, input, author_fix)

    id = strip_value(response, "data", "createReport", "report", "id")
    assert re.match(r"\w+", id)
    snapshot.assert_match(response)

    assert Report.objects.count() == 1
    report = Report.objects.all().values()[0]
    id = strip_value(report, "id")
    snapshot.assert_match(dates_to_iso(report))


def test_input_sanitization(call_api, author_fix):
    input = {
        "title": "<s>No</s> tags",
        "body": 'some <a href="http://foo">link</a> <br>in body',
        "receivedBenefit": "<b>coffee</b>",
        "providedBenefit": "<li>tea",
        "ourParticipants": "me, <u>myself</u>",
        "otherParticipants": "<strong>you!</strong>",
        "date": arrow.utcnow().isoformat(),
    }

    call_api(query, input, author_fix)

    report = Report.objects.get()
    assert report.title == "No tags"
    assert report.body == "some link in body"
    assert report.received_benefit == "coffee"
    assert report.provided_benefit == "tea"
    assert report.our_participants == "me, myself"
    assert report.other_participants == "you!"


@pytest.mark.freeze_time("2018-01-04T00:07:07")
def test_is_draft(call_api, snapshot, author_fix):
    date = arrow.get(2018, 1, 3)
    title = "Visited by old friend"
    body = "Niel deGrasse Tyson just visited me..."
    received_benefit = "touch of the God"
    provided_benefit = "coffee"
    our_participants = "myself"
    other_participants = "Neil deGrasse Tyson"
    input = {
        "title": title,
        "body": body,
        "receivedBenefit": received_benefit,
        "providedBenefit": provided_benefit,
        "ourParticipants": our_participants,
        "otherParticipants": other_participants,
        "date": date.isoformat(),
        "isDraft": True,
    }

    response = call_api(query, input, author_fix)

    id = strip_value(response, "data", "createReport", "report", "id")
    assert re.match(r"\w+", id)
    snapshot.assert_match(response)

    assert Report.objects.count() == 1
    report = Report.objects.all().values()[0]
    id = strip_value(report, "id")
    snapshot.assert_match(dates_to_iso(report))
