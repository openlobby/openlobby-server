# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_login__known_openid_client 1'] = {
    'userinfo': {
        'email': {
            'essential': True
        },
        'family_name': {
            'essential': True
        },
        'given_name': {
            'essential': True
        }
    }
}

snapshots['test_login__new_openid_client 1'] = {
    'userinfo': {
        'email': {
            'essential': True
        },
        'family_name': {
            'essential': True
        },
        'given_name': {
            'essential': True
        }
    }
}
