from elasticsearch_dsl import DocType, Text, Date, Object, Keyword

from .settings import ES_INDEX, ES_TEXT_ANALYZER


class UserDoc(DocType):
    name = Text(analyzer=ES_TEXT_ANALYZER)
    openid_uid = Keyword()
    email = Keyword()
    extra = Object()

    class Meta:
        index = ES_INDEX
        doc_type = 'user'


class ReportDoc(DocType):
    author_id = Keyword()
    date = Date()
    published = Date()
    title = Text(analyzer=ES_TEXT_ANALYZER)
    body = Text(analyzer=ES_TEXT_ANALYZER)
    received_benefit = Text(analyzer=ES_TEXT_ANALYZER)
    provided_benefit = Text(analyzer=ES_TEXT_ANALYZER)
    extra = Object()

    class Meta:
        index = ES_INDEX
        doc_type = 'report'
