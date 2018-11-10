import pytest

from openlobby.core.api.paginator import Paginator, encode_cursor
from openlobby.core.search import search_reports

from .dummy import prepare_reports


pytestmark = [pytest.mark.django_db, pytest.mark.usefixtures("django_es")]


@pytest.mark.parametrize(
    "query, expected_ids",
    [("", [3, 2, 1]), ("sauron", [3, 2]), ("towers", [2]), ("Aragorn Gandalf", [3, 1])],
)
def test_search_reports(query, expected_ids):
    prepare_reports()
    paginator = Paginator()
    response = search_reports(paginator, query=query)
    assert expected_ids == [int(r.meta.id) for r in response]


def test_search_reports__highlight():
    prepare_reports()
    paginator = Paginator()
    query = "King"
    response = search_reports(paginator, query=query, highlight=True)
    doc = response.hits[0]
    assert "<mark>King</mark>" in doc.meta.highlight.title[0]
    assert "<mark>King</mark>" in doc.meta.highlight.body[0]


@pytest.mark.parametrize(
    "first, after, expected_ids", [(2, None, [3, 2]), (2, encode_cursor(1), [2, 1])]
)
def test_search_reports__pagination(first, after, expected_ids):
    prepare_reports()
    query = ""
    paginator = Paginator(first=first, after=after)
    response = search_reports(paginator, query=query)
    assert expected_ids == [int(r.meta.id) for r in response]


def test_search_reports__by_author():
    prepare_reports()
    author_id = 1
    paginator = Paginator()
    response = search_reports(paginator, author_id=author_id)
    assert [3, 1] == [int(r.meta.id) for r in response]


@pytest.mark.parametrize(
    "first, after, expected_ids", [(1, None, [3]), (1, encode_cursor(1), [1])]
)
def test_search_reports__by_author__pagination(first, after, expected_ids):
    prepare_reports()
    author_id = 1
    paginator = Paginator(first=first, after=after)
    response = search_reports(paginator, author_id=author_id)
    assert expected_ids == [int(r.meta.id) for r in response]
