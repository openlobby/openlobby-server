from datetime import datetime
import graphene
from graphene import relay
from graphene.types.datetime import DateTime
from oic.oic import rndstr
from oic.oic.message import AuthorizationResponse
import time
import urllib.parse

from .auth import (
    get_login_attempt_expiration_time,
    get_session_expiration_time,
    create_access_token,
)
from .documents import UserDoc, LoginAttemptDoc, SessionDoc, ReportDoc
from .openid import (
    init_client_for_uid,
    register_client,
    get_authorization_url,
    set_registration_info,
    do_access_token_request,
)
from .types import Report
from .utils import get_viewer


class Login(relay.ClientIDMutation):

    class Input:
        openid_uid = graphene.String(required=True)
        redirect_uri = graphene.String(required=True)

    authorization_url = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        openid_uid = input['openid_uid']
        redirect_uri = input['redirect_uri']

        # prepare OpenID client
        client = init_client_for_uid(openid_uid)
        client = register_client(client, redirect_uri)

        # prepare login attempt details
        state = rndstr(32)
        nonce = rndstr()
        expiration = get_login_attempt_expiration_time()

        # save login attempt into ES
        data = {
            'meta': {'id': client.client_id},
            'state': state,
            'nonce': nonce,
            'client_id': client.client_id,
            'client_secret': client.client_secret,
            'openid_uid': openid_uid,
            'redirect_uri': redirect_uri,
            'expiration': expiration,
        }
        login_attempt = LoginAttemptDoc(**data)
        login_attempt.save(using=info.context['es'])

        # get OpenID authorization url
        authorization_url = get_authorization_url(client, state, nonce)

        return Login(authorization_url=authorization_url)


class LoginRedirect(relay.ClientIDMutation):

    class Input:
        query_string = graphene.String(required=True)

    access_token = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        query_string = input['query_string']

        # get login attempt from ES
        qs_data = urllib.parse.parse_qs(query_string)
        la = LoginAttemptDoc.get(qs_data['client_id'], using=info.context['es'])

        # delete login attempt so it can be used just once
        la.delete(using=info.context['es'])

        # reconstruct OpenID Client
        client = init_client_for_uid(la['openid_uid'])
        client = set_registration_info(client, la['client_id'], la['client_secret'], la['redirect_uri'])

        # process query string from OpenID redirect
        aresp = client.parse_response(AuthorizationResponse, info=query_string, sformat='urlencoded')
        code = aresp['code']
        state = aresp['state']

        # check state
        if state != la['state']:
            raise ValueError('Wrong query_string.')

        # check login attempt expiration
        if la['expiration'] < time.time():
            raise Exception('Login attempt expired.')

        # OpenID access token request
        do_access_token_request(client, code, state)

        # OpenID user info request
        user_info = client.do_user_info_request(state=state)

        # get or create User
        user = UserDoc.get_or_create(info.context['es'], la['openid_uid'], user_info['name'], user_info['email'])

        # create session
        expiration = get_session_expiration_time()
        session = SessionDoc(user_id=user.meta.id, expiration=expiration)
        session.save(using=info.context['es'])

        # create access token for session
        token = create_access_token(session.meta.id, expiration)

        return LoginRedirect(access_token=token)


class NewReport(relay.ClientIDMutation):

    class Input:
        title = graphene.String(required=True)
        body = graphene.String(required=True)
        received_benefit = graphene.String()
        provided_benefit = graphene.String()
        date = DateTime(required=True)

    report = graphene.Field(Report)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        viewer = get_viewer(info)
        if viewer is None:
            raise Exception('User must be logged in to perform this mutation.')
        now = datetime.utcnow()
        report = ReportDoc(published=now, author_id=viewer.id, **input)
        report.save(using=info.context['es'])
        return NewReport(report=Report.from_es(report, author=viewer))


class Mutation(graphene.ObjectType):
    login = Login.Field()
    login_redirect = LoginRedirect.Field()
    new_report = NewReport.Field()
