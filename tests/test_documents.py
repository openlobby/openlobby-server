import time

from openlobby.documents import SessionDoc, UserDoc


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


class TestUserDoc:

    def test_get_by_openid_uid__does_not_exists(self, es, index):
        user = UserDoc.get_by_openid_uid('foo', es=es, index=index)
        assert user is None

    def test_get_by_openid_uid(self, es, index):
        for uid in ['foo', 'bar', 'baz']:
            u = UserDoc(openid_uid=uid)
            u.save(using=es, index=index, refresh='true')
        user = UserDoc.get_by_openid_uid('bar', es=es, index=index)
        assert user is not None
        assert user.openid_uid == 'bar'
