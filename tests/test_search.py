import pytest

from openlobby.core.api.paginator import Paginator, encode_cursor
from openlobby.core.api.schema import REPORT_SORT_DATE_ID, REPORT_SORT_PUBLISHED_ID, REPORT_SORT_RELEVANCE_ID
from openlobby.core.models import Report, User
from openlobby.core.search import query_reports, reports_by_author

from .dummy import prepare_reports, authors, reports

pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures('django_es')]


@pytest.mark.parametrize('query, expected_ids', [
    ('', [3, 2, 1]),
    ('sauron', [3, 2]),
    ('towers', [2]),
    ('Aragorn Gandalf', [3, 1]),
])
def test_query_reports(query, expected_ids):
    prepare_reports()
    paginator = Paginator()
    response = query_reports(query, paginator)
    assert expected_ids == [int(r.meta.id) for r in response]


def test_query_reports__highlight():
    prepare_reports()
    paginator = Paginator()
    query = 'King'
    response = query_reports(query, paginator, highlight=True)
    doc = response.hits[0]
    assert '<mark>King</mark>' in doc.meta.highlight.title[0]
    assert '<mark>King</mark>' in doc.meta.highlight.body[0]


@pytest.mark.parametrize('first, after, expected_ids', [
    (2, None, [3, 2]),
    (2, encode_cursor(1), [2, 1]),
])
def test_query_reports__pagination(first, after, expected_ids):
    prepare_reports()
    query = ''
    paginator = Paginator(first=first, after=after)
    response = query_reports(query, paginator)
    assert expected_ids == [int(r.meta.id) for r in response]


def test_reports_by_author():
    prepare_reports()
    author_id = 1
    paginator = Paginator()
    response = reports_by_author(author_id, paginator)
    assert [3, 1] == [int(r.meta.id) for r in response]


@pytest.mark.parametrize('first, after, expected_ids', [
    (1, None, [3]),
    (1, encode_cursor(1), [1]),
])
def test_reports_by_author__pagination(first, after, expected_ids):
    prepare_reports()
    author_id = 1
    paginator = Paginator(first=first, after=after)
    response = reports_by_author(author_id, paginator)
    assert expected_ids == [int(r.meta.id) for r in response]


@pytest.mark.parametrize('query, expected_ids', [
    ('', [3, 2, 1]),
    ('sauron', [3, 2]),
    ('towers', [2]),
    ('Aragorn Gandalf', [3, 1]),
])
def test_query_reports_sort_date(query, expected_ids):
    prepare_reports()
    paginator = Paginator()
    response = query_reports(query, paginator, sort=REPORT_SORT_DATE_ID)
    assert expected_ids == [int(r.meta.id) for r in response]

    response = query_reports(query, paginator, sort=REPORT_SORT_DATE_ID, reversed=False)
    assert expected_ids == [int(r.meta.id) for r in response]

    # reversing expected_ids, notice ...reversed(response)
    response = query_reports(query, paginator, sort=REPORT_SORT_DATE_ID, reversed=True)
    assert expected_ids == [int(r.meta.id) for r in reversed(response)]


@pytest.mark.parametrize('query, expected_ids', [
    ('Gandalf', [1, 6]),
])
def test_query_reports_sort_published(query, expected_ids):
    prepare_reports()
    author4 = User.objects.create(**authors[3])
    Report.objects.create(author=author4, **reports[5])

    paginator = Paginator()
    response = query_reports(query, paginator, sort=REPORT_SORT_PUBLISHED_ID)
    assert expected_ids == [int(r.meta.id) for r in response]

    response = query_reports(query, paginator, sort=REPORT_SORT_PUBLISHED_ID, reversed=False)
    assert expected_ids == [int(r.meta.id) for r in response]

    # reversing expected_ids, notice ...reversed(response)
    response = query_reports(query, paginator, sort=REPORT_SORT_PUBLISHED_ID, reversed=True)
    assert expected_ids == [int(r.meta.id) for r in reversed(response)]

@pytest.mark.parametrize('query, expected_ids', [
    ('Gandalf', [6, 1])
])
def test_query_reports_sort_date(query, expected_ids):
    prepare_reports()
    author4 = User.objects.create(**authors[3])
    Report.objects.create(author=author4, **reports[5])

    paginator = Paginator()
    response = query_reports(query, paginator, sort=REPORT_SORT_DATE_ID)
    assert expected_ids == [int(r.meta.id) for r in response]

    response = query_reports(query, paginator, sort=REPORT_SORT_DATE_ID, reversed=False)
    assert expected_ids == [int(r.meta.id) for r in response]

    # reversing expected_ids, notice ...reversed(response)
    response = query_reports(query, paginator, sort=REPORT_SORT_DATE_ID, reversed=True)
    assert expected_ids == [int(r.meta.id) for r in reversed(response)]

@pytest.mark.parametrize('query, expected_ids', [
    ('Gandalf', [6, 1]),
    ('story', [6, 2, 1]),
])
def test_query_reports_sort_relevance(query, expected_ids):
    prepare_reports()
    author4 = User.objects.create(**authors[3])
    Report.objects.create(author=author4, **reports[5])

    paginator = Paginator()
    response = query_reports(query, paginator, sort=REPORT_SORT_RELEVANCE_ID)
    assert expected_ids == [int(r.meta.id) for r in response]

    response = query_reports(query, paginator, sort=REPORT_SORT_RELEVANCE_ID, reversed=False)
    assert expected_ids == [int(r.meta.id) for r in response]

    # reversing expected_ids, notice ...reversed(response)
    response = query_reports(query, paginator, sort=REPORT_SORT_RELEVANCE_ID, reversed=True)
    assert expected_ids == [int(r.meta.id) for r in reversed(response)]