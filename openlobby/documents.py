from elasticsearch_dsl import DocType, Text, Date, Object, Keyword, Integer, Boolean
import time

from .settings import ES_TEXT_ANALYZER


"""
Don't forget to add a new document to the list of all documents at the end of
the file.
"""


class UserDoc(DocType):
    openid_uid = Keyword()
    name = Text(analyzer=ES_TEXT_ANALYZER)
    email = Keyword()
    extra = Object()

    class Meta:
        doc_type = 'user'

    @classmethod
    def get_by_openid_uid(cls, openid_uid, *, es, index):
        response = cls.search(using=es, index=index).query('match', openid_uid=openid_uid).execute()
        return response.hits[0] if response.hits.total > 0 else None


class ReportDoc(DocType):
    author_id = Keyword()
    date = Date()
    published = Date()
    title = Text(analyzer=ES_TEXT_ANALYZER)
    body = Text(analyzer=ES_TEXT_ANALYZER)
    received_benefit = Text(analyzer=ES_TEXT_ANALYZER)
    provided_benefit = Text(analyzer=ES_TEXT_ANALYZER)
    our_participants = Text(analyzer=ES_TEXT_ANALYZER)
    other_participants = Text(analyzer=ES_TEXT_ANALYZER)
    extra = Object()

    class Meta:
        doc_type = 'report'


class OpenIdClientDoc(DocType):
    # TODO conflict in field type
    name_x = Keyword()
    is_shortcut = Boolean()
    client_id = Keyword()
    client_secret = Keyword()
    issuer = Keyword()
    authorization_endpoint = Keyword()
    token_endpoint = Keyword()
    userinfo_endpoint = Keyword()

    class Meta:
        doc_type = 'open-id-client'


class LoginAttemptDoc(DocType):
    openid_uid = Keyword()
    redirect_uri = Keyword()
    state = Keyword()
    nonce = Keyword()
    client_id = Keyword()
    client_secret = Keyword()
    expiration = Integer()  # UTC timestamp

    class Meta:
        doc_type = 'login-attempt'


class SessionDoc(DocType):
    user_id = Keyword()
    expiration = Integer()  # UTC timestamp

    class Meta:
        doc_type = 'session'

    @classmethod
    def get_active(cls, session_id, *, es, index):
        session = cls.get(session_id, using=es, index=index, ignore=404)
        if session and session.expiration > time.time():
            return session
        return None


all_documents = (
    UserDoc,
    ReportDoc,
    LoginAttemptDoc,
    SessionDoc,
    OpenIdClientDoc,
)
