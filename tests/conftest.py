import pytest
from pytest_factoryboy import register
from django_elasticsearch_dsl.test import ESTestCase
import json

from openlobby.core.auth import create_access_token

from . import factories

register(factories.UserFactory)
register(factories.AuthorFactory)
register(factories.ReportFactory)


class DummyTestCase:
    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestCase(ESTestCase, DummyTestCase):
    pass


@pytest.fixture
def django_es():
    """Setup and teardown of Elasticsearch test indices."""
    testCase = TestCase()
    testCase.setUp()
    yield
    testCase.tearDown()


def pytest_addoption(parser):
    parser.addoption(
        "--issuer",
        action="store",
        help="OpenID Provider (server) issuer URL. Provider must allow client registration.",
    )


@pytest.fixture(scope="session")
def issuer(request):
    """OpenID Provider issuer URL."""
    url = request.config.getoption("--issuer")
    if url is None:
        pytest.skip("Missing OpenID Provider URL.")
    return url


@pytest.fixture
def author_fix(author_factory):
    return author_factory(
        id=42,
        username="wolfe",
        first_name="Winston",
        last_name="Wolfe",
        extra={"caliber": 45},
        email="winston@wolfe.com",
        openid_uid="TheWolf",
    )


@pytest.fixture
def call_api(client):
    def _call_api(query, input=None, user=None):
        variables = json.dumps({"input": input or {}})
        payload = {"query": query, "variables": variables}
        if user is None:
            res = client.post("/graphql", payload)
        else:
            token = create_access_token(user.username)
            auth_header = "Bearer {}".format(token)
            res = client.post("/graphql", payload, HTTP_AUTHORIZATION=auth_header)
        return res.json()

    return _call_api
