import os
from flask import Flask
from elasticsearch import Elasticsearch

from .auth import AuthGraphQLView
from .management import bootstrap_es
from .schema import schema
from .settings import ES_INDEX


app = Flask(__name__)


es_dsn = os.environ.get('ELASTICSEARCH_DSN', 'http://localhost:9200')
es_client = Elasticsearch(es_dsn)

bootstrap_es(es_client, ES_INDEX)


@app.route('/')
def hello():
    return 'Open Lobby Server\n\nAPI is at: /graphql', 200, {'Content-Type': 'text/plain; charset=utf-8'}


app.add_url_rule('/graphql', view_func=AuthGraphQLView.as_view(
    'graphql', schema=schema, graphiql=True, context={'es': es_client, 'index': ES_INDEX}))
