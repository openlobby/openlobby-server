from elasticsearch import Elasticsearch
import os
import pytest
import random
import string


from openlobby.management import init_alias


@pytest.fixture(scope='session')
def es():
    """Elasticsearch client."""
    es_dsn = os.environ.get('ELASTICSEARCH_DSN', 'http://localhost:9200')
    es_client = Elasticsearch(es_dsn)
    yield es_client
    es_client.indices.delete('test_*')


@pytest.fixture
def index_name():
    """Random test index name."""
    length = 10
    word = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    return 'test_{}'.format(word)


@pytest.fixture
def index(es, index_name):
    """Initialized index."""
    init_alias(es, index_name)
    return index_name
