# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_all 1'] = {
    'data': {
        'authors': {
            'edges': [
                {
                    'cursor': 'MQ==',
                    'node': {
                        'extra': None,
                        'firstName': 'Shaun',
                        'hasCollidingName': False,
                        'id': 'QXV0aG9yOjM=',
                        'lastName': 'Sheep',
                        'totalReports': 0
                    }
                },
                {
                    'cursor': 'Mg==',
                    'node': {
                        'extra': None,
                        'firstName': 'Spongebob',
                        'hasCollidingName': False,
                        'id': 'QXV0aG9yOjI=',
                        'lastName': 'Squarepants',
                        'totalReports': 0
                    }
                },
                {
                    'cursor': 'Mw==',
                    'node': {
                        'extra': '{"movies": 1}',
                        'firstName': 'Winston',
                        'hasCollidingName': False,
                        'id': 'QXV0aG9yOjE=',
                        'lastName': 'Wolfe',
                        'totalReports': 0
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'Mw==',
                'hasNextPage': False,
                'hasPreviousPage': False,
                'startCursor': 'MQ=='
            },
            'totalCount': 3
        }
    }
}

snapshots['test_first 1'] = {
    'data': {
        'authors': {
            'edges': [
                {
                    'cursor': 'MQ==',
                    'node': {
                        'extra': None,
                        'firstName': 'Shaun',
                        'hasCollidingName': False,
                        'id': 'QXV0aG9yOjM=',
                        'lastName': 'Sheep',
                        'totalReports': 0
                    }
                },
                {
                    'cursor': 'Mg==',
                    'node': {
                        'extra': None,
                        'firstName': 'Spongebob',
                        'hasCollidingName': False,
                        'id': 'QXV0aG9yOjI=',
                        'lastName': 'Squarepants',
                        'totalReports': 0
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'Mg==',
                'hasNextPage': True,
                'hasPreviousPage': False,
                'startCursor': 'MQ=='
            },
            'totalCount': 3
        }
    }
}

snapshots['test_first_after 1'] = {
    'data': {
        'authors': {
            'edges': [
                {
                    'cursor': 'Mg==',
                    'node': {
                        'extra': None,
                        'firstName': 'Spongebob',
                        'hasCollidingName': False,
                        'id': 'QXV0aG9yOjI=',
                        'lastName': 'Squarepants',
                        'totalReports': 0
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'Mg==',
                'hasNextPage': True,
                'hasPreviousPage': True,
                'startCursor': 'Mg=='
            },
            'totalCount': 3
        }
    }
}

snapshots['test_last 1'] = {
    'data': {
        'authors': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 9,
                    'line': 3
                }
            ],
            'message': 'Pagination "last" works only in combination with "before" argument.'
        }
    ]
}

snapshots['test_last_before 1'] = {
    'data': {
        'authors': {
            'edges': [
                {
                    'cursor': 'Mg==',
                    'node': {
                        'extra': None,
                        'firstName': 'Spongebob',
                        'hasCollidingName': False,
                        'id': 'QXV0aG9yOjI=',
                        'lastName': 'Squarepants',
                        'totalReports': 0
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'Mg==',
                'hasNextPage': True,
                'hasPreviousPage': True,
                'startCursor': 'Mg=='
            },
            'totalCount': 3
        }
    }
}

snapshots['test_with_reports 1'] = {
    'data': {
        'authors': {
            'edges': [
                {
                    'node': {
                        'extra': '{"movies": 1}',
                        'firstName': 'Winston',
                        'hasCollidingName': False,
                        'id': 'QXV0aG9yOjE=',
                        'lastName': 'Wolfe',
                        'reports': {
                            'edges': [
                                {
                                    'cursor': 'MQ==',
                                    'node': {
                                        'body': 'Long story short: we got the Ring!',
                                        'date': '2018-01-01 00:00:00+00:00',
                                        'extra': None,
                                        'id': 'UmVwb3J0OjE=',
                                        'otherParticipants': 'Saruman',
                                        'ourParticipants': 'Frodo, Gandalf',
                                        'providedBenefit': '',
                                        'published': '2018-01-02 00:00:00+00:00',
                                        'receivedBenefit': 'The Ring',
                                        'title': 'The Fellowship of the Ring'
                                    }
                                }
                            ],
                            'totalCount': 1
                        },
                        'totalReports': 1
                    }
                }
            ]
        }
    }
}
