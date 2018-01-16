import time

from ..documents import SessionDoc


class TestSessionDoc:

    def test_get_active__does_not_exists(self, es, index):
        session = SessionDoc.get_active('foo', es=es, index=index)
        assert session is None

    def test_get_active__expired(self, es, index):
        s = SessionDoc(user_id='foo', expiration=123456789)
        s.save(using=es, index=index)
        session = SessionDoc.get_active(s.meta.id, es=es, index=index)
        assert session is None

    def test_get_active(self, es, index):
        expiration = time.time() + 100
        s = SessionDoc(user_id='foo', expiration=expiration)
        s.save(using=es, index=index, refresh='true')
        session = SessionDoc.get_active(s.meta.id, es=es, index=index)
        assert session is not None
        assert session.user_id == 'foo'
        assert session.expiration == expiration
