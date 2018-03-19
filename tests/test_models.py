from unittest.mock import patch

import arrow
import pytest
from django.conf import settings
from openlobby.core.api.schema import AUTHOR_SORT_LAST_NAME_ID, AUTHOR_SORT_TOTAL_REPORTS_ID
from openlobby.core.documents import ReportDoc
from openlobby.core.models import Report, User, OpenIdClient, LoginAttempt

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures('django_es')]


def test_report__marks_user_as_author_on_save():
    author = User.objects.create(id=1, is_author=False)
    date = arrow.get(2018, 1, 1).datetime
    Report.objects.create(author=author, date=date, body='Lorem ipsum.')
    user = User.objects.get(id=1)
    assert user.is_author


def test_report__marks_user_as_author_on_save__not_if_draft():
    author = User.objects.create(id=1, is_author=False)
    date = arrow.get(2018, 1, 1).datetime
    Report.objects.create(author=author, is_draft=True, date=date, body='Lorem ipsum.')
    user = User.objects.get(id=1)
    assert not user.is_author


def test_report__is_saved_in_elasticsearch():
    author = User.objects.create(id=6)
    date = arrow.get(2018, 1, 1).datetime
    published = arrow.get(2018, 1, 2).datetime
    Report.objects.create(
        id=3,
        author=author,
        date=date,
        published=published,
        title='It happened',
        body='Lorem ipsum.',
        received_benefit='coffee',
        provided_benefit='tea',
        our_participants='me',
        other_participants='them',
        extra={'a': 3},
        is_draft=False,
    )
    docs = list(ReportDoc.search())
    assert len(docs) == 1
    doc = docs[0]
    assert doc.meta.id == '3'
    assert doc.author_id == 6
    assert doc.date == date
    assert doc.published == published
    assert doc.title == 'It happened'
    assert doc.body == 'Lorem ipsum.'
    assert doc.received_benefit == 'coffee'
    assert doc.provided_benefit == 'tea'
    assert doc.our_participants == 'me'
    assert doc.other_participants == 'them'
    assert doc.extra == {'a': 3}
    assert not doc.is_draft


def test_report__save_works_with_no_extra():
    author = User.objects.create(id=6)
    date = arrow.get(2018, 1, 1).datetime
    Report.objects.create(
        id=7,
        author=author,
        date=date,
        published=date,
        body='Lorem ipsum.',
    )
    docs = list(ReportDoc.search())
    assert len(docs) == 1
    doc = docs[0]
    assert doc.meta.id == '7'
    assert doc.extra is None


def test_login_attempt__default_expiration():
    client = OpenIdClient.objects.create(name='a', client_id='b', client_secret='c')
    with patch('openlobby.core.models.time.time', return_value=10000):
        attempt = LoginAttempt.objects.create(openid_client=client, state='foo',
                                              app_redirect_uri='http://openlobby/app')
    assert attempt.expiration == 10000 + settings.LOGIN_ATTEMPT_EXPIRATION


def test_user__no_name_collision():
    User.objects.create(username='a', is_author=True, first_name='Ryan', last_name='Gosling')
    User.objects.create(username='b', is_author=True, first_name='Ryan', last_name='Reynolds')
    assert User.objects.get(username='a').has_colliding_name is False
    assert User.objects.get(username='b').has_colliding_name is False


def test_user__name_collision():
    User.objects.create(username='a', is_author=True, first_name='Ryan', last_name='Gosling')
    User.objects.create(username='b', is_author=True, first_name='Ryan', last_name='Gosling')
    assert User.objects.get(username='a').has_colliding_name is True
    assert User.objects.get(username='b').has_colliding_name is True


def test_user__name_collision_affects_only_authors():
    User.objects.create(username='a', is_author=False, first_name='Ryan', last_name='Gosling')
    User.objects.create(username='b', is_author=True, first_name='Ryan', last_name='Gosling')
    User.objects.create(username='c', is_author=False, first_name='Ryan', last_name='Gosling')
    assert User.objects.get(username='a').has_colliding_name is False
    assert User.objects.get(username='b').has_colliding_name is False
    assert User.objects.get(username='c').has_colliding_name is False
    User.objects.create(username='d', is_author=True, first_name='Ryan', last_name='Gosling')
    assert User.objects.get(username='a').has_colliding_name is False
    assert User.objects.get(username='b').has_colliding_name is True
    assert User.objects.get(username='c').has_colliding_name is False
    assert User.objects.get(username='d').has_colliding_name is True


def test_user__name_collision_excludes_self_on_update():
    u = User.objects.create(username='a', is_author=True, first_name='Ryan', last_name='Gosling')
    u.save()
    assert User.objects.get(username='a').has_colliding_name is False


def test_user__sorted_default():
    User.objects.create(username='a', is_author=False, first_name='Ryan', last_name='AGosling')
    User.objects.create(username='b', is_author=True, first_name='Ryan', last_name='BGosling')
    User.objects.create(username='c', is_author=False, first_name='Ryan', last_name='CGosling')
    assert User.objects.sorted()[0].username == 'a'


def test_user__sorted_default_reversed():
    User.objects.create(username='a', is_author=False, first_name='Ryan', last_name='AGosling')
    User.objects.create(username='b', is_author=True, first_name='Ryan', last_name='BGosling')
    User.objects.create(username='c', is_author=False, first_name='Ryan', last_name='CGosling')
    assert User.objects.sorted(reversed=True)[0].username == 'c'


def test_user__sorted_last_name():
    User.objects.create(username='a', is_author=False, first_name='Ryan', last_name='AGosling')
    User.objects.create(username='b', is_author=True, first_name='Ryan', last_name='BGosling')
    User.objects.create(username='c', is_author=False, first_name='Ryan', last_name='CGosling')
    assert User.objects.sorted(sort=AUTHOR_SORT_LAST_NAME_ID)[0].username == 'a'
    assert User.objects.sorted(sort=AUTHOR_SORT_LAST_NAME_ID, reversed=False)[0].username == 'a'
    assert User.objects.sorted(sort=AUTHOR_SORT_LAST_NAME_ID, reversed=True)[0].username == 'c'


def test_user__sorted_total_reports():
    author = User.objects.create(username='a', is_author=True, first_name='Ryan', last_name='AGosling')
    User.objects.create(username='b', is_author=True, first_name='Ryan', last_name='BGosling')
    date = arrow.get(2018, 1, 1).datetime
    Report.objects.create(
        id=7,
        author=author,
        date=date,
        published=date,
        body='Lorem ipsum.',
    )
    assert User.objects.sorted(sort=AUTHOR_SORT_TOTAL_REPORTS_ID)[0].username == 'a'
    assert User.objects.sorted(sort=AUTHOR_SORT_TOTAL_REPORTS_ID, reversed=False)[0].username == 'a'
    assert User.objects.sorted(sort=AUTHOR_SORT_TOTAL_REPORTS_ID, reversed=True)[0].username == 'b'
