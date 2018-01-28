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
    """Setup and teardown of test indices."""
    testCase = TestCase()
    testCase.setUp()
    yield
    testCase.tearDown()
