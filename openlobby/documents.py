from elasticsearch_dsl import DocType, Text, Date, Object, Keyword, Integer

from .settings import ES_INDEX, ES_TEXT_ANALYZER


class UserDoc(DocType):
    openid_uid = Keyword()
    name = Text(analyzer=ES_TEXT_ANALYZER)
    email = Keyword()
    extra = Object()

    class Meta:
        index = ES_INDEX
        doc_type = 'user'

    @classmethod
    def get_or_create(cls, using, openid_uid, name, email):
        response = cls.search(using=using).query('match', openid_uid=openid_uid).execute()
        if response.hits.total == 0:
            user = UserDoc(openid_uid=openid_uid, name=name, email=email)
            user.save(using=using)
        else:
            user = response.hits[0]
        return user


class ReportDoc(DocType):
    author_id = Keyword()
    date = Date()
    published = Date()
    title = Text(analyzer=ES_TEXT_ANALYZER)
    body = Text(analyzer=ES_TEXT_ANALYZER)
    received_benefit = Text(analyzer=ES_TEXT_ANALYZER)
    provided_benefit = Text(analyzer=ES_TEXT_ANALYZER)
    extra = Object()

    class Meta:
        index = ES_INDEX
        doc_type = 'report'


class LoginAttemptDoc(DocType):
    openid_uid = Keyword()
    redirect_uri = Keyword()
    state = Keyword()
    nonce = Keyword()
    client_id = Keyword()
    client_secret = Keyword()
    expiration = Integer()  # UTC timestamp

    class Meta:
        index = ES_INDEX
        doc_type = 'login-attempt'


class SessionDoc(DocType):
    user_id = Keyword()
    expiration = Integer()  # UTC timestamp

    class Meta:
        index = ES_INDEX
        doc_type = 'session'
