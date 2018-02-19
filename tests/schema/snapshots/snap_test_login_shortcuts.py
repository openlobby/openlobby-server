# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_returns_only_shortcuts 1'] = {
    'data': {
        'loginShortcuts': [
            {
                'id': 'TG9naW5TaG9ydGN1dDoyMA==',
                'name': 'bar'
            }
        ]
    }
}

snapshots['test_none 1'] = {
    'data': {
        'loginShortcuts': [
        ]
    }
}
