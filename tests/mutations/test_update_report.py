import pytest
import arrow
from graphql_relay import to_global_id
from unittest.mock import patch

from openlobby.core.models import Report

from ..utils import dates_to_iso, strip_value


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("django_es")]


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
            edited
            hasRevisions
            revisions {
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
            }
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

original_edited = arrow.get(2018, 1, 2, 5)
edited = original_edited.shift(minutes=50)
late_edited = original_edited.shift(minutes=70)


@pytest.fixture
def original_report(author_fix, report_factory):
    return report_factory(
        id=666,
        author=author_fix,
        date=arrow.get(2018, 1, 1).datetime,
        published=arrow.get(2018, 1, 2).datetime,
        edited=original_edited.datetime,
        title="Original",
        body="Previous body.",
        received_benefit="old coffee",
        provided_benefit="old tea",
        our_participants="grandpa",
        other_participants="grandma",
    )


@pytest.fixture
def original_report_draft(original_report):
    original_report.is_draft = True
    original_report.save()
    return original_report


def prepare_input(is_draft=False, id=1):
    return {
        "id": to_global_id("Report", id),
        "title": "New title",
        "body": "Rewrited",
        "receivedBenefit": "cake",
        "providedBenefit": "water",
        "ourParticipants": "kids",
        "otherParticipants": "grandchilds",
        "date": arrow.get(2018, 3, 3).isoformat(),
        "isDraft": is_draft,
    }


def test_unauthorized(call_api, snapshot, original_report):
    input = prepare_input(id=original_report.id)
    response = call_api(query, input)
    snapshot.assert_match(response)


def test_not_author(call_api, snapshot, original_report, user):
    input = prepare_input(id=original_report.id)
    response = call_api(query, input, user)
    snapshot.assert_match(response)


def test_report_does_not_exist(call_api, snapshot, author_fix):
    input = prepare_input(id=789)
    response = call_api(query, input, author_fix)
    snapshot.assert_match(response)


def test_update_published_with_draft(call_api, snapshot, original_report):
    input = prepare_input(id=original_report.id, is_draft=True)
    response = call_api(query, input, original_report.author)
    snapshot.assert_match(response)


def test_update_draft_with_draft(call_api, snapshot, original_report_draft):
    input = prepare_input(id=original_report_draft.id, is_draft=True)

    with patch("openlobby.core.api.mutations.arrow.utcnow", return_value=edited):
        response = call_api(query, input, original_report_draft.author)

    snapshot.assert_match(response)
    reports = list(map(dates_to_iso, Report.objects.all().values()))
    snapshot.assert_match(reports)


def test_update_draft_with_draft__late_edit(call_api, snapshot, original_report_draft):
    input = prepare_input(id=original_report_draft.id, is_draft=True)

    with patch("openlobby.core.api.mutations.arrow.utcnow", return_value=late_edited):
        response = call_api(query, input, original_report_draft.author)

    snapshot.assert_match(response)
    reports = list(map(dates_to_iso, Report.objects.all().values()))
    snapshot.assert_match(reports)


def test_update_draft_with_published(call_api, snapshot, original_report_draft):
    input = prepare_input(id=original_report_draft.id)

    with patch("openlobby.core.api.mutations.arrow.utcnow", return_value=edited):
        response = call_api(query, input, original_report_draft.author)

    snapshot.assert_match(response)
    reports = list(map(dates_to_iso, Report.objects.all().values()))
    snapshot.assert_match(reports)


def test_update_draft_with_published__late_edit(
    call_api, snapshot, original_report_draft
):
    input = prepare_input(id=original_report_draft.id)

    with patch("openlobby.core.api.mutations.arrow.utcnow", return_value=late_edited):
        response = call_api(query, input, original_report_draft.author)

    snapshot.assert_match(response)
    reports = list(map(dates_to_iso, Report.objects.all().values()))
    snapshot.assert_match(reports)


def test_update_published_with_published(call_api, snapshot, original_report):
    input = prepare_input(id=original_report.id)

    with patch("openlobby.core.api.mutations.arrow.utcnow", return_value=edited):
        response = call_api(query, input, original_report.author)

    snapshot.assert_match(response)
    reports = list(map(dates_to_iso, Report.objects.all().values()))
    snapshot.assert_match(reports)


def test_update_published_with_published__late_edit(
    call_api, snapshot, original_report
):
    input = prepare_input(id=original_report.id)

    with patch("openlobby.core.api.mutations.arrow.utcnow", return_value=late_edited):
        response = call_api(query, input, original_report.author)

    strip_value(response, "data", "updateReport", "report", "revisions", "id")
    snapshot.assert_match(response)
    assert Report.objects.count() == 2
    updated = Report.objects.filter(id=original_report.id).values()[0]
    original = Report.objects.filter(superseded_by_id=original_report.id).values()[0]
    strip_value(original, "id")
    snapshot.assert_match(dates_to_iso(updated))
    snapshot.assert_match(dates_to_iso(original))


def test_input_sanitization(call_api, snapshot, original_report):
    input = {
        "id": to_global_id("Report", original_report.id),
        "title": "<s>No</s> tags",
        "body": 'some <a href="http://foo">link</a> <br>in body',
        "receivedBenefit": "<b>coffee</b>",
        "providedBenefit": "<li>tea",
        "ourParticipants": "me, <u>myself</u>",
        "otherParticipants": "<strong>you!</strong>",
        "date": arrow.get(2018, 3, 3).isoformat(),
    }

    with patch("openlobby.core.api.mutations.arrow.utcnow", return_value=edited):
        response = call_api(query, input, original_report.author)

    snapshot.assert_match(response)
    reports = list(map(dates_to_iso, Report.objects.all().values()))
    snapshot.assert_match(reports)
