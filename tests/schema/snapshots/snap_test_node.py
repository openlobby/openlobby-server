# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_login_shortcut 1'] = {
    'data': {
        'node': {
            'id': 'TG9naW5TaG9ydGN1dDoxMA==',
            'name': 'foo'
        }
    }
}

snapshots['test_author 1'] = {
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

snapshots['test_author__returns_only_if_is_author 1'] = {
    'data': {
        'node': None
    }
}

snapshots['test_report 1'] = {
    'data': {
        'node': {
            'author': {
                'extra': None,
                'firstName': 'Winston',
                'id': 'QXV0aG9yOjE=',
                'lastName': 'Wolfe'
            },
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
}
