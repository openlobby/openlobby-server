import os
from flask import Flask
from flask_graphql import GraphQLView
from elasticsearch import Elasticsearch

from .schema import schema
from .documents import AuthorDoc, ReportDoc


es_dsn = os.environ.get('ELASTICSEARCH_DSN', 'http://localhost:9200')
es_client = Elasticsearch(es_dsn)


AuthorDoc.init(using=es_client)
ReportDoc.init(using=es_client)

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Open Lobby Server\n\nAPI is at: /graphql', 200, {'Content-Type': 'text/plain; charset=utf-8'}


app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql', schema=schema, graphiql=True, context={'es': es_client}
))
