from elasticsearch_dsl import DocType, Text, Date, Object, Keyword

from .constants import ES_INDEX


class AuthorDoc(DocType):
    name = Text()
    extra = Object()

    class Meta:
        index = ES_INDEX
        doc_type = 'author'


class ReportDoc(DocType):
    author_id = Keyword()
    date = Date()
    published = Date()
    title = Text()
    body = Text()
    received_benefit = Text()
    provided_benefit = Text()
    extra = Object()

    class Meta:
        index = ES_INDEX
        doc_type = 'report'
