import pytest
import dsnparse
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
    parser.addoption('--keycloak', action='store',
        help=('Keycloak server DSN with OpenID client credentials for auth tests.'
              ' Format: http://client_id:client_secret@host:port/realm'))


@pytest.fixture(scope='session')
def keycloak(request):
    """Keycloak server and OpenID client info."""
    dsn = request.config.getoption('--keycloak')
    if dsn is None:
        pytest.skip('No Keycloak DSN provided.')

    config = dsnparse.parse(dsn)
    realm_url = '{}://{}:{}/auth/realms/{}'.format(config.scheme, config.host, config.port, config.paths[0])
    return {
        'client_id': config.username,
        'client_secret': config.password,
        'issuer': realm_url,
    }
