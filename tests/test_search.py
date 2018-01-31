import pytest
import arrow

from openlobby.core.api.paginator import Paginator, encode_cursor
from openlobby.core.models import Report, User
from openlobby.core.search import query_reports


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures('django_es')]


reports = [
    {
        'id': 1,
        'date': arrow.get(2018, 1, 1).datetime,
        'published': arrow.get(2018, 1, 2).datetime,
        'title': 'The Fellowship of the Ring',
        'body': 'Long story short: we got the Ring!',
        'received_benefit': 'The Ring',
        'provided_benefit': '',
        'our_participants': 'Frodo, Gandalf',
        'other_participants': 'Saruman',
    },
    {
        'id': 2,
        'date': arrow.get(2018, 1, 5).datetime,
        'published': arrow.get(2018, 1, 10).datetime,
        'title': 'The Two Towers',
        'body': 'Another long story.',
        'received_benefit': 'Mithrill Jacket',
        'provided_benefit': '',
        'our_participants': 'Frodo, Gimli, Legolas',
        'other_participants': 'Saruman, Sauron',
    },
    {
        'id': 3,
        'date': arrow.get(2018, 1, 7).datetime,
        'published': arrow.get(2018, 1, 8).datetime,
        'title': 'The Return of the King',
        'body': 'Aragorn is the King. And we have lost the Ring.',
        'received_benefit': '',
        'provided_benefit': 'The Ring',
        'our_participants': 'Aragorn',
        'other_participants': 'Sauron',
    },
]


def prepare_data():
    author = User.objects.create(id=1, username='Wolf', openid_uid='Wolf',
        first_name='Winston', last_name='Wolfe')
    for report in reports:
        Report.objects.create(author=author, **report)


@pytest.mark.parametrize('query, expected_ids', [
    ('', [2, 3, 1]),
    ('sauron', [2, 3]),
    ('towers', [2]),
    ('Aragorn Gandalf', [3, 1]),
])
def test_query_reports(query, expected_ids):
    prepare_data()
    paginator = Paginator()
    response = query_reports(query, paginator)
    assert expected_ids == [int(r.meta.id) for r in response]


def test_query_reports__highlight():
    prepare_data()
    paginator = Paginator()
    query = 'King'
    response = query_reports(query, paginator, highlight=True)
    doc = response.hits[0]
    assert '<mark>King</mark>' in doc.meta.highlight.title[0]
    assert '<mark>King</mark>' in doc.meta.highlight.body[0]


@pytest.mark.parametrize('first, after, expected_ids', [
    (2, None, [2, 3]),
    (2, encode_cursor(1), [3, 1]),
])
def test_query_reports__pagination(first, after, expected_ids):
    prepare_data()
    query = ''
    paginator = Paginator(first=first, after=after)
    response = query_reports(query, paginator)
    assert expected_ids == [int(r.meta.id) for r in response]
