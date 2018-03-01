# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_unauthorized 1'] = {
    'data': {
        'createReport': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 5,
                    'line': 3
                }
            ],
            'message': 'User must be logged in to perform this mutation.'
        }
    ]
}

snapshots['test_full_report 1'] = {
    'data': {
        'createReport': {
            'report': {
                'author': {
                    'extra': '{"movies": 1}',
                    'firstName': 'Winston',
                    'id': 'QXV0aG9yOjE=',
                    'lastName': 'Wolfe',
                    'totalReports': 1
                },
                'body': 'I visited Tesla factory and talked with Elon Musk.',
                'date': '2018-01-01 00:00:00+00:00',
                'extra': None,
                'id': '__STRIPPED__',
                'isDraft': False,
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

snapshots['test_is_draft 1'] = {
    'data': {
        'createReport': {
            'report': {
                'author': {
                    'extra': '{"movies": 1}',
                    'firstName': 'Winston',
                    'id': 'QXV0aG9yOjE=',
                    'lastName': 'Wolfe',
                    'totalReports': 0
                },
                'body': 'Niel deGrasse Tyson just visited me...',
                'date': '2018-01-03 00:00:00+00:00',
                'extra': None,
                'id': '__STRIPPED__',
                'isDraft': True,
                'otherParticipants': 'Neil deGrasse Tyson',
                'ourParticipants': 'myself',
                'providedBenefit': 'coffee',
                'published': '__STRIPPED__',
                'receivedBenefit': 'touch of the God',
                'title': 'Visited by old friend'
            }
        }
    }
}
