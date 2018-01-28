import pytest
import arrow

from openlobby.core.models import Report, User
from openlobby.core.documents import ReportDoc


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures('django_es')]


def test_report_marks_user_as_author_on_save():
    author = User.objects.create(id=1, is_author=False)
    date = arrow.get(2018, 1, 1).datetime
    Report.objects.create(author=author, date=date, body='Lorem ipsum.')
    user = User.objects.get(id=1)
    assert user.is_author


def test_report_is_saved_in_elasticsearch():
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
    assert doc.get_extra() == {'a': 3}
