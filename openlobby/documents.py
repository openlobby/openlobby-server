from elasticsearch_dsl import DocType, Text, Date, Object, Keyword

from .settings import ES_INDEX


class AuthorDoc(DocType):
    name = Text(analyzer='czech')
    extra = Object()

    class Meta:
        index = ES_INDEX
        doc_type = 'author'


class ReportDoc(DocType):
    author_id = Keyword()
    date = Date()
    published = Date()
    title = Text(analyzer='czech')
    body = Text(analyzer='czech')
    received_benefit = Text(analyzer='czech')
    provided_benefit = Text(analyzer='czech')
    extra = Object()

    class Meta:
        index = ES_INDEX
        doc_type = 'report'
