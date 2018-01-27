# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_login_shortcuts__none 1'] = b'{"data":{"loginShortcuts":[]}}'

snapshots['test_login_shortcuts 1'] = b'{"data":{"loginShortcuts":[{"id":"TG9naW5TaG9ydGN1dDoyMA==","name":"bar"}]}}'

snapshots['test_node__login_shortcut 1'] = b'{"data":{"node":{"id":"TG9naW5TaG9ydGN1dDoxMA==","name":"foo"}}}'

snapshots['test_node__author 1'] = b'{"data":{"node":{"id":"QXV0aG9yOjU=","name":"Winston Wolfe","openidUid":"TheWolf","extra":"{\\"x\\": 1}"}}}'

snapshots['test_node__author__only_if_is_author 1'] = b'{"data":{"node":null}}'
