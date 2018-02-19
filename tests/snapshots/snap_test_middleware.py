# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_wrong_header 1'] = {
    'errors': [
        {
            'message': 'Wrong Authorization header. Expected: "Bearer <token>"'
        }
    ]
}

snapshots['test_invalid_token 1'] = {
    'errors': [
        {
            'message': 'Invalid Token.'
        }
    ]
}
