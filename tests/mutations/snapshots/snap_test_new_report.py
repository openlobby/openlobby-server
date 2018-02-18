# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_unauthorized 1'] = {
    'data': {
        'newReport': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 9,
                    'line': 3
                }
            ],
            'message': 'User must be logged in to perform this mutation.'
        }
    ]
}

snapshots['test_full_report 1'] = {
    'data': {
        'newReport': {
            'report': {
                'author': {
                    'extra': None,
                    'firstName': 'Winston',
                    'id': 'QXV0aG9yOjE=',
                    'lastName': 'Wolfe'
                },
                'body': 'I visited Tesla factory and talked with Elon Musk.',
                'date': '2018-01-01 00:00:00+00:00',
                'extra': None,
                'id': '__STRIPPED__',
                'otherParticipants': 'Elon Musk',
                'ourParticipants': 'me',
                'providedBenefit': 'nothing',
                'published': '__STRIPPED__',
                'receivedBenefit': 'Tesla Model S',
                'title': 'Free Tesla'
            }
        }
    }
}
