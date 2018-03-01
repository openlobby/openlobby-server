# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_all 1'] = {
    'data': {
        'searchReports': {
            'edges': [
                {
                    'cursor': 'MQ==',
                    'node': {
                        'author': {
                            'extra': '{"movies": 1}',
                            'firstName': 'Winston',
                            'hasCollidingName': False,
                            'id': 'QXV0aG9yOjE=',
                            'lastName': 'Wolfe',
                            'totalReports': 2
                        },
                        'body': 'Aragorn is the King. And we have lost the Ring.',
                        'date': '2018-01-05 00:00:00+00:00',
                        'extra': None,
                        'id': 'UmVwb3J0OjM=',
                        'isDraft': False,
                        'otherParticipants': 'Sauron',
                        'ourParticipants': 'Aragorn',
                        'providedBenefit': 'The Ring',
                        'published': '2018-01-06 00:00:00+00:00',
                        'receivedBenefit': '',
                        'title': 'The Return of the King'
                    }
                },
                {
                    'cursor': 'Mg==',
                    'node': {
                        'author': {
                            'extra': None,
                            'firstName': 'Spongebob',
                            'hasCollidingName': False,
                            'id': 'QXV0aG9yOjI=',
                            'lastName': 'Squarepants',
                            'totalReports': 1
                        },
                        'body': 'Another long story.',
                        'date': '2018-01-03 00:00:00+00:00',
                        'extra': '{"rings": 1}',
                        'id': 'UmVwb3J0OjI=',
                        'isDraft': False,
                        'otherParticipants': 'Saruman, Sauron',
                        'ourParticipants': 'Frodo, Gimli, Legolas',
                        'providedBenefit': '',
                        'published': '2018-01-04 00:00:00+00:00',
                        'receivedBenefit': 'Mithrill Jacket',
                        'title': 'The Two Towers'
                    }
                },
                {
                    'cursor': 'Mw==',
                    'node': {
                        'author': {
                            'extra': '{"movies": 1}',
                            'firstName': 'Winston',
                            'hasCollidingName': False,
                            'id': 'QXV0aG9yOjE=',
                            'lastName': 'Wolfe',
                            'totalReports': 2
                        },
                        'body': 'Long story short: we got the Ring!',
                        'date': '2018-01-01 00:00:00+00:00',
                        'extra': None,
                        'id': 'UmVwb3J0OjE=',
                        'isDraft': False,
                        'otherParticipants': 'Saruman',
                        'ourParticipants': 'Frodo, Gandalf',
                        'providedBenefit': '',
                        'published': '2018-01-02 00:00:00+00:00',
                        'receivedBenefit': 'The Ring',
                        'title': 'The Fellowship of the Ring'
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

snapshots['test_query 1'] = {
    'data': {
        'searchReports': {
            'edges': [
                {
                    'cursor': 'MQ==',
                    'node': {
                        'author': {
                            'extra': None,
                            'firstName': 'Spongebob',
                            'hasCollidingName': False,
                            'id': 'QXV0aG9yOjI=',
                            'lastName': 'Squarepants',
                            'totalReports': 1
                        },
                        'body': 'Another long story.',
                        'date': '2018-01-03 00:00:00+00:00',
                        'extra': '{"rings": 1}',
                        'id': 'UmVwb3J0OjI=',
                        'isDraft': False,
                        'otherParticipants': 'Saruman, Sauron',
                        'ourParticipants': 'Frodo, Gimli, Legolas',
                        'providedBenefit': '',
                        'published': '2018-01-04 00:00:00+00:00',
                        'receivedBenefit': 'Mithrill Jacket',
                        'title': 'The Two Towers'
                    }
                }
            ],
            'totalCount': 1
        }
    }
}

snapshots['test_highlight 1'] = {
    'data': {
        'searchReports': {
            'edges': [
                {
                    'cursor': 'MQ==',
                    'node': {
                        'author': {
                            'extra': '{"movies": 1}',
                            'firstName': 'Winston',
                            'hasCollidingName': False,
                            'id': 'QXV0aG9yOjE=',
                            'lastName': 'Wolfe',
                            'totalReports': 2
                        },
                        'body': 'Aragorn is the King. And we have lost the <mark>Ring</mark>.',
                        'date': '2018-01-05 00:00:00+00:00',
                        'extra': None,
                        'id': 'UmVwb3J0OjM=',
                        'isDraft': False,
                        'otherParticipants': 'Sauron',
                        'ourParticipants': 'Aragorn',
                        'providedBenefit': 'The <mark>Ring</mark>',
                        'published': '2018-01-06 00:00:00+00:00',
                        'receivedBenefit': '',
                        'title': 'The Return of the King'
                    }
                },
                {
                    'cursor': 'Mg==',
                    'node': {
                        'author': {
                            'extra': '{"movies": 1}',
                            'firstName': 'Winston',
                            'hasCollidingName': False,
                            'id': 'QXV0aG9yOjE=',
                            'lastName': 'Wolfe',
                            'totalReports': 2
                        },
                        'body': 'Long story short: we got the <mark>Ring</mark>!',
                        'date': '2018-01-01 00:00:00+00:00',
                        'extra': None,
                        'id': 'UmVwb3J0OjE=',
                        'isDraft': False,
                        'otherParticipants': 'Saruman',
                        'ourParticipants': 'Frodo, Gandalf',
                        'providedBenefit': '',
                        'published': '2018-01-02 00:00:00+00:00',
                        'receivedBenefit': 'The <mark>Ring</mark>',
                        'title': 'The Fellowship of the <mark>Ring</mark>'
                    }
                }
            ],
            'totalCount': 2
        }
    }
}

snapshots['test_first 1'] = {
    'data': {
        'searchReports': {
            'edges': [
                {
                    'cursor': 'MQ==',
                    'node': {
                        'id': 'UmVwb3J0OjM=',
                        'title': 'The Return of the King'
                    }
                }
            ],
            'pageInfo': {
                'endCursor': 'MQ==',
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
        'searchReports': {
            'edges': [
                {
                    'cursor': 'Mg==',
                    'node': {
                        'id': 'UmVwb3J0OjI=',
                        'title': 'The Two Towers'
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
        'searchReports': None
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
        'searchReports': {
            'edges': [
                {
                    'cursor': 'Mg==',
                    'node': {
                        'id': 'UmVwb3J0OjI=',
                        'title': 'The Two Towers'
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
