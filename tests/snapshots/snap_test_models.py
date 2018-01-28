# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot, GenericRepr


snapshots = Snapshot()

snapshots['test_report_is_saved_in_elasticsearch 1'] = [
    GenericRepr("ReportDoc(index='report_ded_test', doc_type='report_doc', id='2')")
]
