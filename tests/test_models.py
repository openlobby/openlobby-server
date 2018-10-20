from unittest.mock import patch

import arrow
import pytest
from django.conf import settings
from openlobby.core.documents import ReportDoc
from openlobby.core.models import Report, User, OpenIdClient, LoginAttempt, UserSort

from .dummy import prepare_reports

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("django_es")]


def test_report__marks_user_as_author_on_save():
    author = User.objects.create(id=1, is_author=False)
    date = arrow.get(2018, 1, 1).datetime
    Report.objects.create(author=author, date=date, body="Lorem ipsum.")
    user = User.objects.get(id=1)
    assert user.is_author


def test_report__marks_user_as_author_on_save__not_if_draft():
    author = User.objects.create(id=1, is_author=False)
    date = arrow.get(2018, 1, 1).datetime
    Report.objects.create(author=author, is_draft=True, date=date, body="Lorem ipsum.")
    user = User.objects.get(id=1)
    assert not user.is_author


def test_report__is_saved_in_elasticsearch():
    author = User.objects.create(id=6)
    date = arrow.get(2018, 1, 1).datetime
    published = arrow.get(2018, 1, 2).datetime
    edited = arrow.get(2018, 1, 3).datetime
    replacement = Report.objects.create(id=4, author=author, date=date, body="IDDQD")
    Report.objects.create(
        id=3,
        author=author,
        date=date,
        published=published,
        edited=edited,
        title="It happened",
        body="Lorem ipsum.",
        received_benefit="coffee",
        provided_benefit="tea",
        our_participants="me",
        other_participants="them",
        extra={"a": 3},
        is_draft=False,
        superseded_by=replacement,
    )
    docs = list(ReportDoc.search())
    assert len(docs) == 2
    doc = docs[1]
    assert doc.meta.id == "3"
    assert doc.author_id == 6
    assert doc.superseded_by_id == 4
    assert doc.date == date
    assert doc.published == published
    assert doc.edited == edited
    assert doc.title == "It happened"
    assert doc.body == "Lorem ipsum."
    assert doc.received_benefit == "coffee"
    assert doc.provided_benefit == "tea"
    assert doc.our_participants == "me"
    assert doc.other_participants == "them"
    assert doc.extra == {"a": 3}
    assert not doc.is_draft


def test_report__save_works_with_no_extra():
    author = User.objects.create(id=6)
    date = arrow.get(2018, 1, 1).datetime
    Report.objects.create(
        id=7, author=author, date=date, published=date, body="Lorem ipsum."
    )
    docs = list(ReportDoc.search())
    assert len(docs) == 1
    doc = docs[0]
    assert doc.meta.id == "7"
    assert doc.extra is None


def test_login_attempt__default_expiration():
    client = OpenIdClient.objects.create(name="a", client_id="b", client_secret="c")
    with patch("openlobby.core.models.time.time", return_value=10000):
        attempt = LoginAttempt.objects.create(
            openid_client=client, state="foo", app_redirect_uri="http://openlobby/app"
        )
    assert attempt.expiration == 10000 + settings.LOGIN_ATTEMPT_EXPIRATION


def test_user__no_name_collision():
    User.objects.create(
        username="a", is_author=True, first_name="Ryan", last_name="Gosling"
    )
    User.objects.create(
        username="b", is_author=True, first_name="Ryan", last_name="Reynolds"
    )
    assert User.objects.get(username="a").has_colliding_name is False
    assert User.objects.get(username="b").has_colliding_name is False


def test_user__name_collision():
    User.objects.create(
        username="a", is_author=True, first_name="Ryan", last_name="Gosling"
    )
    User.objects.create(
        username="b", is_author=True, first_name="Ryan", last_name="Gosling"
    )
    assert User.objects.get(username="a").has_colliding_name is True
    assert User.objects.get(username="b").has_colliding_name is True


def test_user__name_collision_affects_only_authors():
    User.objects.create(
        username="a", is_author=False, first_name="Ryan", last_name="Gosling"
    )
    User.objects.create(
        username="b", is_author=True, first_name="Ryan", last_name="Gosling"
    )
    User.objects.create(
        username="c", is_author=False, first_name="Ryan", last_name="Gosling"
    )
    assert User.objects.get(username="a").has_colliding_name is False
    assert User.objects.get(username="b").has_colliding_name is False
    assert User.objects.get(username="c").has_colliding_name is False
    User.objects.create(
        username="d", is_author=True, first_name="Ryan", last_name="Gosling"
    )
    assert User.objects.get(username="a").has_colliding_name is False
    assert User.objects.get(username="b").has_colliding_name is True
    assert User.objects.get(username="c").has_colliding_name is False
    assert User.objects.get(username="d").has_colliding_name is True


def test_user__name_collision_excludes_self_on_update():
    u = User.objects.create(
        username="a", is_author=True, first_name="Ryan", last_name="Gosling"
    )
    u.save()
    assert User.objects.get(username="a").has_colliding_name is False


@pytest.mark.parametrize(
    "params, expected",
    [
        ({}, ["Sheep", "Squarepants", "Wolfe"]),
        ({"reversed": False}, ["Sheep", "Squarepants", "Wolfe"]),
        ({"reversed": True}, ["Wolfe", "Squarepants", "Sheep"]),
        ({"sort": UserSort.LAST_NAME}, ["Sheep", "Squarepants", "Wolfe"]),
        (
            {"sort": UserSort.LAST_NAME, "reversed": False},
            ["Sheep", "Squarepants", "Wolfe"],
        ),
        (
            {"sort": UserSort.LAST_NAME, "reversed": True},
            ["Wolfe", "Squarepants", "Sheep"],
        ),
        ({"sort": UserSort.TOTAL_REPORTS}, ["Wolfe", "Sheep", "Squarepants"]),
        (
            {"sort": UserSort.TOTAL_REPORTS, "reversed": False},
            ["Wolfe", "Sheep", "Squarepants"],
        ),
        (
            {"sort": UserSort.TOTAL_REPORTS, "reversed": True},
            ["Squarepants", "Sheep", "Wolfe"],
        ),
    ],
)
def test_user__sorted(params, expected):
    prepare_reports()
    last_names = User.objects.sorted(**params).values_list("last_name", flat=True)
    assert list(last_names) == expected


def test_user__with_total_reports():
    prepare_reports()
    users = User.objects.with_total_reports().values_list("last_name", "total_reports")
    assert set(users) == {("Wolfe", 2), ("Sheep", 1), ("Squarepants", 0)}
