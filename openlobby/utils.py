from flask import g

from .documents import SessionDoc
from .types import User


def get_viewer(info):
    """Resolves actual viewer and caches it into 'g'."""
    if not hasattr(g, 'viewer'):
        session_id = g.get('session_id', None)
        if session_id is None:
            g.viewer = None
        else:
            session = SessionDoc.get_active(session_id, **info.context)
            if session is None:
                g.viewer = None
            else:
                g.viewer = User.get_node(info, session.user_id)
    return g.viewer
