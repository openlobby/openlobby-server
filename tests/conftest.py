from elasticsearch import Elasticsearch
import os
import pytest
import random
import string


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
