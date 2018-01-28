# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_login_shortcuts__none 1'] = {
    'data': {
        'loginShortcuts': [
        ]
    }
}

snapshots['test_login_shortcuts 1'] = {
    'data': {
        'loginShortcuts': [
            {
                'id': 'TG9naW5TaG9ydGN1dDoyMA==',
                'name': 'bar'
            }
        ]
    }
}

snapshots['test_node__login_shortcut 1'] = {
    'data': {
        'node': {
            'id': 'TG9naW5TaG9ydGN1dDoxMA==',
            'name': 'foo'
        }
    }
}

snapshots['test_node__author 1'] = {
    'data': {
        'node': {
            'extra': '{"x": 1}',
            'firstName': 'Winston',
            'id': 'QXV0aG9yOjU=',
            'lastName': 'Wolfe',
            'openidUid': 'TheWolf'
        }
    }
}

snapshots['test_node__author__only_if_is_author 1'] = {
    'data': {
        'node': None
    }
}

snapshots['TestAuthors.test_all 1'] = {
    'data': {
        'authors': {
            'edges': [
                {
                    'cursor': 'MQ==',
                    'node': {
                        'extra': '{"x": 1}',
                        'firstName': 'Winston',
                        'id': 'QXV0aG9yOjE=',
                        'lastName': 'Wolfe',
                        'openidUid': 'TheWolf'
                    }
                },
                {
                    'cursor': 'Mg==',
                    'node': {
                        'extra': None,
                        'firstName': 'Captain',
                        'id': 'QXV0aG9yOjM=',
                        'lastName': 'Obvious',
                        'openidUid': 'ccc'
                    }
                },
                {
                    'cursor': 'Mw==',
                    'node': {
                        'extra': None,
                        'firstName': 'Shaun',
                        'id': 'QXV0aG9yOjQ=',
                        'lastName': 'Sheep',
                        'openidUid': 'ddd'
                    }
                }
            ],
            'totalCount': 3
        }
    }
}
