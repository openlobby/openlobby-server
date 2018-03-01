# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_unauthorized 1'] = {
    'data': {
        'updateReport': None
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

snapshots['test_not_author 1'] = {
    'data': {
        'updateReport': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 5,
                    'line': 3
                }
            ],
            'message': 'Viewer is not the Author of this Report or Report does not exist.'
        }
    ]
}

snapshots['test_report_does_not_exist 1'] = {
    'data': {
        'updateReport': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 5,
                    'line': 3
                }
            ],
            'message': 'Viewer is not the Author of this Report or Report does not exist.'
        }
    ]
}

snapshots['test_update_published_with_draft 1'] = {
    'data': {
        'updateReport': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 5,
                    'line': 3
                }
            ],
            'message': 'You cannot update published Report with draft.'
        }
    ]
}

snapshots['test_update_draft_with_draft 1'] = {
    'data': {
        'updateReport': {
            'report': {
                'author': {
                    'extra': '{"movies": 1}',
                    'firstName': 'Winston',
                    'id': 'QXV0aG9yOjE=',
                    'lastName': 'Wolfe',
                    'totalReports': 0
                },
                'body': 'I visited Tesla factory and talked with Elon Musk.',
                'date': '2018-03-03 00:00:00+00:00',
                'extra': None,
                'id': 'UmVwb3J0OjE=',
                'isDraft': True,
                'otherParticipants': 'Elon Musk',
                'ourParticipants': 'me',
                'providedBenefit': 'nothing',
                'published': '2018-03-08 00:00:00+00:00',
                'receivedBenefit': 'Tesla Model S',
                'title': 'Free Tesla'
            }
        }
    }
}

snapshots['test_update_draft_with_published 1'] = {
    'data': {
        'updateReport': {
            'report': {
                'author': {
                    'extra': '{"movies": 1}',
                    'firstName': 'Winston',
                    'id': 'QXV0aG9yOjE=',
                    'lastName': 'Wolfe',
                    'totalReports': 1
                },
                'body': 'I visited Tesla factory and talked with Elon Musk.',
                'date': '2018-03-03 00:00:00+00:00',
                'extra': None,
                'id': 'UmVwb3J0OjE=',
                'isDraft': False,
                'otherParticipants': 'Elon Musk',
                'ourParticipants': 'me',
                'providedBenefit': 'nothing',
                'published': '2018-03-08 00:00:00+00:00',
                'receivedBenefit': 'Tesla Model S',
                'title': 'Free Tesla'
            }
        }
    }
}

snapshots['test_update_published_with_published 1'] = {
    'data': {
        'updateReport': {
            'report': {
                'author': {
                    'extra': '{"movies": 1}',
                    'firstName': 'Winston',
                    'id': 'QXV0aG9yOjE=',
                    'lastName': 'Wolfe',
                    'totalReports': 1
                },
                'body': 'I visited Tesla factory and talked with Elon Musk.',
                'date': '2018-03-03 00:00:00+00:00',
                'extra': None,
                'id': 'UmVwb3J0OjE=',
                'isDraft': False,
                'otherParticipants': 'Elon Musk',
                'ourParticipants': 'me',
                'providedBenefit': 'nothing',
                'published': '2018-03-08 00:00:00+00:00',
                'receivedBenefit': 'Tesla Model S',
                'title': 'Free Tesla'
            }
        }
    }
}

snapshots['test_input_sanitization 1'] = {
    'data': {
        'updateReport': {
            'report': {
                'author': {
                    'extra': '{"movies": 1}',
                    'firstName': 'Winston',
                    'id': 'QXV0aG9yOjE=',
                    'lastName': 'Wolfe',
                    'totalReports': 1
                },
                'body': 'some link in body',
                'date': '2018-03-03 00:00:00+00:00',
                'extra': None,
                'id': 'UmVwb3J0OjE=',
                'isDraft': False,
                'otherParticipants': 'you!',
                'ourParticipants': 'me, myself',
                'providedBenefit': 'tea',
                'published': '2018-03-08 00:00:00+00:00',
                'receivedBenefit': 'coffee',
                'title': 'No tags'
            }
        }
    }
}
