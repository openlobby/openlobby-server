import arrow
import graphene
from graphene import relay
from graphene.types.datetime import DateTime
from graphql_relay import from_global_id
from oic.oic import rndstr
from oic.oic.message import AuthorizationResponse
import time
import urllib.parse

from ..auth import (
    get_login_attempt_expiration_time,
    get_session_expiration_time,
    create_access_token,
)
from ..documents import (
    SessionDoc,
    ReportDoc,
)
from ..models import OpenIdClient, LoginAttempt
from ..openid import (
    init_client_for_uid,
    init_client_for_shortcut,
    register_client,
    get_authorization_url,
    set_registration_info,
    do_access_token_request,
)
from ..utils import get_viewer
from .types import Report
from .sanitizers import strip_all_tags


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
        try:
            openid_client_obj = OpenIdClient.objects.get(issuer=client.provider_info['issuer'])
            client = init_client_for_shortcut(openid_client_obj, redirect_uri)
        except OpenIdClient.DoesNotExist:
            client = register_client(client, redirect_uri)
            openid_client_obj = OpenIdClient.objects.create(
                name=client.provider_info['issuer'],
                client_id=client.client_id,
                client_secret=client.client_secret,
                issuer=client.provider_info['issuer'],
                authorization_endpoint=client.provider_info['authorization_endpoint'],
                token_endpoint=client.provider_info['token_endpoint'],
                userinfo_endpoint=client.provider_info['userinfo_endpoint'],
            )

        # prepare login attempt details
        state = rndstr(48)
        expiration = get_login_attempt_expiration_time()

        # save login attempt
        LoginAttempt.objects.create(state=state, openid_client=openid_client_obj,
            expiration=expiration, redirect_uri=redirect_uri)

        # get OpenID authorization url
        authorization_url = get_authorization_url(client, state)

        return Login(authorization_url=authorization_url)


class LoginByShortcut(relay.ClientIDMutation):

    class Input:
        shortcut_id = relay.GlobalID(required=True)
        redirect_uri = graphene.String(required=True)

    authorization_url = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        shortcut_id = input['shortcut_id']
        redirect_uri = input['redirect_uri']

        # prepare OpenID client
        type, id = from_global_id(shortcut_id)
        openid_client_obj = OpenIdClient.objects.get(id=id)
        client = init_client_for_shortcut(openid_client_obj, redirect_uri)

        # prepare login attempt
        state = rndstr(48)
        expiration = get_login_attempt_expiration_time()

        # save login attempt
        LoginAttempt.objects.create(state=state, openid_client=openid_client_obj,
            expiration=expiration, redirect_uri=redirect_uri)

        # get OpenID authorization url
        authorization_url = get_authorization_url(client, state)

        return LoginByShortcut(authorization_url=authorization_url)


class LoginRedirect(relay.ClientIDMutation):

    class Input:
        query_string = graphene.String(required=True)

    access_token = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        query_string = input['query_string']

        # get state from query string
        state = urllib.parse.parse_qs(query_string)['state'][0]
        print('X:', state)

        # get login attempt
        la = LoginAttempt.objects.select_related().get(state=state)

        # delete login attempt so it can be used just once
        # TODO uncomment
        #la.delete()

        # check login attempt expiration
        if la.expiration < time.time():
            raise Exception('Login attempt expired.')

        # reconstruct OpenID Client
        client = init_client_for_shortcut(la.openid_client, la.redirect_uri)

        # process query string from OpenID redirect
        aresp = client.parse_response(AuthorizationResponse, info=query_string,
            sformat='urlencoded')
        code = aresp['code']
        state = aresp['state']

        # OpenID access token request
        do_access_token_request(client, code, state)

        # OpenID user info request
        user_info = client.do_user_info_request(state=state)
        print(user_info)

        """
        # get or create User
        user = UserDoc.get_by_openid_uid(la['openid_uid'], **info.context)
        if user is None:
            user = UserDoc(openid_uid=la['openid_uid'], name=user_info['name'], email=user_info['email'])
            user.save(using=info.context['es'], index=info.context['index'])

        # create session
        expiration = get_session_expiration_time()
        session = SessionDoc(user_id=user.meta.id, expiration=expiration)
        session.save(using=info.context['es'], index=info.context['index'])

        # create access token for session
        token = create_access_token(session.meta.id, expiration)
        """
        token = 'foo'

        return LoginRedirect(access_token=token)


class Logout(relay.ClientIDMutation):
    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        viewer = get_viewer(info)
        if viewer is None:
            raise Exception('User must be logged in to perform this mutation.')

        # TODO
        raise NotImplementedError()
        session_id = g.get('session_id')
        session = SessionDoc.get(session_id, using=info.context['es'], index=info.context['index'])
        session.delete(using=info.context['es'], index=info.context['index'])

        return Logout(success=True)


class NewReport(relay.ClientIDMutation):

    class Input:
        title = graphene.String(required=True)
        body = graphene.String(required=True)
        received_benefit = graphene.String()
        provided_benefit = graphene.String()
        our_participants = graphene.String()
        other_participants = graphene.String()
        date = DateTime(required=True)

    report = graphene.Field(Report)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        viewer = get_viewer(info)
        if viewer is None:
            raise Exception('User must be logged in to perform this mutation.')

        data = {
            'author_id': viewer.id,
            'published': arrow.utcnow().isoformat(),
            'title': strip_all_tags(input.get('title', '')),
            'body': strip_all_tags(input.get('body', '')),
            'received_benefit': strip_all_tags(input.get('received_benefit', '')),
            'provided_benefit': strip_all_tags(input.get('provided_benefit', '')),
            'our_participants': strip_all_tags(input.get('our_participants', '')),
            'other_participants': strip_all_tags(input.get('other_participants', '')),
            'date': input.get('date'),
        }
        report = ReportDoc(**data)
        report.save(using=info.context['es'], index=info.context['index'])
        return NewReport(report=Report.from_es(report, author=viewer))


class Mutation:
    login = Login.Field()
    login_by_shortcut = LoginByShortcut.Field()
    login_redirect = LoginRedirect.Field()
    logout = Logout.Field()
    new_report = NewReport.Field()
