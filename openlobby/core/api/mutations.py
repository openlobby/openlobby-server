import arrow
import graphene
from graphene import relay
from graphene.types.datetime import DateTime
from graphql_relay import from_global_id
from oic.oic import rndstr

from ..documents import ReportDoc
from ..models import OpenIdClient, LoginAttempt
from ..openid import (
    init_client_for_uid,
    init_client_for_shortcut,
    register_client,
    get_authorization_url,
)
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
        app_redirect_uri = input['redirect_uri']

        # prepare OpenID client
        client = init_client_for_uid(openid_uid)
        try:
            openid_client_obj = OpenIdClient.objects.get(issuer=client.provider_info['issuer'])
            client = init_client_for_shortcut(openid_client_obj)
        except OpenIdClient.DoesNotExist:
            client = register_client(client)
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

        # save login attempt
        LoginAttempt.objects.create(state=state, openid_client=openid_client_obj,
            app_redirect_uri=app_redirect_uri)

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
        app_redirect_uri = input['redirect_uri']

        # prepare OpenID client
        type, id = from_global_id(shortcut_id)
        openid_client_obj = OpenIdClient.objects.get(id=id)
        client = init_client_for_shortcut(openid_client_obj)

        # prepare login attempt
        state = rndstr(48)

        # save login attempt
        LoginAttempt.objects.create(state=state, openid_client=openid_client_obj,
            app_redirect_uri=app_redirect_uri)

        # get OpenID authorization url
        authorization_url = get_authorization_url(client, state)

        return LoginByShortcut(authorization_url=authorization_url)


class Logout(relay.ClientIDMutation):
    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # TODO
        raise NotImplementedError()
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
        if not info.context.user.is_authenticated:
            raise Exception('User must be logged in to perform this mutation.')

        author = info.context.user

        data = {
            'author_id': author.id,
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
        return NewReport(report=Report.from_es(report, author=author))


class Mutation:
    login = Login.Field()
    login_by_shortcut = LoginByShortcut.Field()
    logout = Logout.Field()
    new_report = NewReport.Field()
