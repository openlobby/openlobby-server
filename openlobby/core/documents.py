from django.conf import settings
from elasticsearch_dsl import DocType, Text, Date, Object, Keyword


class ReportDoc(DocType):
    author_id = Keyword()
    date = Date()
    published = Date()
    title = Text(analyzer=settings.ES_TEXT_ANALYZER)
    body = Text(analyzer=settings.ES_TEXT_ANALYZER)
    received_benefit = Text(analyzer=settings.ES_TEXT_ANALYZER)
    provided_benefit = Text(analyzer=settings.ES_TEXT_ANALYZER)
    our_participants = Text(analyzer=settings.ES_TEXT_ANALYZER)
    other_participants = Text(analyzer=settings.ES_TEXT_ANALYZER)
    extra = Object()

    class Meta:
        doc_type = 'report'


all_documents = (
    ReportDoc,
)
