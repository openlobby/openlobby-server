from django.conf import settings
from django_elasticsearch_dsl import DocType, Index, fields
import json

from .models import Report


report = Index('{}-reports'.format(settings.ES_INDEX))


@report.doc_type
class ReportDoc(DocType):
    author_id = fields.IntegerField()
    title = fields.TextField(analyzer=settings.ES_TEXT_ANALYZER)
    body = fields.TextField(analyzer=settings.ES_TEXT_ANALYZER)
    received_benefit = fields.TextField(analyzer=settings.ES_TEXT_ANALYZER)
    provided_benefit = fields.TextField(analyzer=settings.ES_TEXT_ANALYZER)
    our_participants = fields.TextField(analyzer=settings.ES_TEXT_ANALYZER)
    other_participants = fields.TextField(analyzer=settings.ES_TEXT_ANALYZER)
    # there is no support for JSONField now, so we serialize it to keyword
    extra_serialized = fields.KeywordField()

    def prepare_extra_serialized(self, instance):
        return json.dumps(instance.extra)

    @property
    def extra(self):
        return json.loads(self.extra_serialized)

    class Meta:
        model = Report

        fields = [
            'date',
            'published',
            'is_draft',
        ]
