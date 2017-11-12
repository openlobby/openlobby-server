import os
from flask import Flask
from flask_graphql import GraphQLView
from elasticsearch import Elasticsearch

from .bootstrap import bootstrap_es
from .schema import schema


app = Flask(__name__)

es_dsn = os.environ.get('ELASTICSEARCH_DSN', 'http://localhost:9200')
es_client = Elasticsearch(es_dsn)

bootstrap_es(es_client)


@app.route('/')
def hello():
    return 'Open Lobby Server\n\nAPI is at: /graphql', 200, {'Content-Type': 'text/plain; charset=utf-8'}


app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql', schema=schema, graphiql=True, context={'es': es_client}
))
