from django.conf import settings
from django_elasticsearch_dsl import DocType, Index, fields

from .models import Report


report = Index('report')


@report.doc_type
class ReportDoc(DocType):
    author_id = fields.IntegerField()
    title = fields.TextField(analyzer=settings.ES_TEXT_ANALYZER)
    body = fields.TextField(analyzer=settings.ES_TEXT_ANALYZER)
    received_benefit = fields.TextField(analyzer=settings.ES_TEXT_ANALYZER)
    provided_benefit = fields.TextField(analyzer=settings.ES_TEXT_ANALYZER)
    our_participants = fields.TextField(analyzer=settings.ES_TEXT_ANALYZER)
    other_participants = fields.TextField(analyzer=settings.ES_TEXT_ANALYZER)
    extra = fields.ObjectField()

    class Meta:
        model = Report

        fields = [
            'date',
            'published',
        ]
