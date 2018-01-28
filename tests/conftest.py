from elasticsearch import Elasticsearch
import os
import pytest


@pytest.fixture(scope='session')
def es():
    """Elasticsearch client."""
    es_dsn = os.environ.get('ELASTICSEARCH_DSN', 'http://localhost:9200')
    es_client = Elasticsearch(es_dsn)
    yield es_client
    es_client.indices.delete('test_*')
