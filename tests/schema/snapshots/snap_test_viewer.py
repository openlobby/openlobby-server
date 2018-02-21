# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_unauthenticated 1'] = {
    'data': {
        'viewer': None
    }
}

snapshots['test_authenticated 1'] = {
    'data': {
        'viewer': {
            'email': 'winston@wolfe.com',
            'extra': '{"caliber": 45}',
            'firstName': 'Winston',
            'hasCollidingName': False,
            'id': 'VXNlcjox',
            'isAuthor': True,
            'lastName': 'Wolfe',
            'openidUid': 'TheWolf'
        }
    }
}

snapshots['test_wrong_header 1'] = {
    'errors': [
        {
            'message': 'Wrong Authorization header. Expected: "Bearer <token>"'
        }
    ]
}

snapshots['test_wrong_token 1'] = {
    'errors': [
        {
            'message': 'Invalid Token.'
        }
    ]
}

snapshots['test_unknown_user 1'] = {
    'data': {
        'viewer': None
    }
}
