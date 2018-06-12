import pytest
from django_elasticsearch_dsl.test import ESTestCase


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
