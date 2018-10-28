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
            'message': 'User must be logged in to perform this mutation.',
            'path': [
                'createReport'
            ]
        }
    ]
}

snapshots['test_full_report 1'] = {
    'data': {
        'createReport': {
            'report': {
                'author': {
                    'extra': '{"caliber": 45}',
                    'firstName': 'Winston',
                    'id': 'QXV0aG9yOjQy',
                    'lastName': 'Wolfe',
                    'totalReports': 1
                },
                'body': 'I visited Tesla factory and talked with Elon Musk.',
                'date': '2018-01-01 00:00:00+00:00',
                'edited': '2018-01-01 01:02:03+00:00',
                'extra': None,
                'id': '__STRIPPED__',
                'isDraft': False,
                'otherParticipants': 'Elon Musk',
                'ourParticipants': 'me',
                'providedBenefit': 'nothing',
                'published': '2018-01-01 01:02:03+00:00',
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
                    'extra': '{"caliber": 45}',
                    'firstName': 'Winston',
                    'id': 'QXV0aG9yOjQy',
                    'lastName': 'Wolfe',
                    'totalReports': 0
                },
                'body': 'Niel deGrasse Tyson just visited me...',
                'date': '2018-01-03 00:00:00+00:00',
                'edited': '2018-01-04 00:07:07+00:00',
                'extra': None,
                'id': '__STRIPPED__',
                'isDraft': True,
                'otherParticipants': 'Neil deGrasse Tyson',
                'ourParticipants': 'myself',
                'providedBenefit': 'coffee',
                'published': '2018-01-04 00:07:07+00:00',
                'receivedBenefit': 'touch of the God',
                'title': 'Visited by old friend'
            }
        }
    }
}

snapshots['test_full_report 2'] = {
    'author_id': 42,
    'body': 'I visited Tesla factory and talked with Elon Musk.',
    'date': '2018-01-01T00:00:00+00:00',
    'edited': '2018-01-01T01:02:03+00:00',
    'extra': None,
    'id': '__STRIPPED__',
    'is_draft': False,
    'other_participants': 'Elon Musk',
    'our_participants': 'me',
    'provided_benefit': 'nothing',
    'published': '2018-01-01T01:02:03+00:00',
    'received_benefit': 'Tesla Model S',
    'superseded_by_id': None,
    'title': 'Free Tesla'
}

snapshots['test_is_draft 2'] = {
    'author_id': 42,
    'body': 'Niel deGrasse Tyson just visited me...',
    'date': '2018-01-03T00:00:00+00:00',
    'edited': '2018-01-04T00:07:07+00:00',
    'extra': None,
    'id': '__STRIPPED__',
    'is_draft': True,
    'other_participants': 'Neil deGrasse Tyson',
    'our_participants': 'myself',
    'provided_benefit': 'coffee',
    'published': '2018-01-04T00:07:07+00:00',
    'received_benefit': 'touch of the God',
    'superseded_by_id': None,
    'title': 'Visited by old friend'
}
