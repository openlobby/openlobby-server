import arrow
import graphene
from graphene import relay
from graphene.types.datetime import DateTime
from graphql_relay import from_global_id
from oic.oic import rndstr

from ..models import OpenIdClient, LoginAttempt, Report
from ..openid import (
    discover_issuer,
    init_client_for_shortcut,
    register_client,
    get_authorization_url,
)
from . import types
from .sanitizers import strip_all_tags


STATE_LENGTH = 48


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
        issuer = discover_issuer(openid_uid)
        try:
            openid_client_obj = OpenIdClient.objects.get(issuer=issuer)
            client = init_client_for_shortcut(openid_client_obj)
        except OpenIdClient.DoesNotExist:
            client = register_client(issuer)
            openid_client_obj = OpenIdClient.objects.create(
                name=issuer,
                issuer=issuer,
                client_id=client.client_id,
                client_secret=client.client_secret,
            )

        # prepare login attempt details
        state = rndstr(STATE_LENGTH)

        # save login attempt
        LoginAttempt.objects.create(state=state, openid_client=openid_client_obj,
            app_redirect_uri=app_redirect_uri, openid_uid=openid_uid)

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
        state = rndstr(STATE_LENGTH)

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
        raise NotImplementedError()
        return Logout(success=True)


class CreateReport(relay.ClientIDMutation):

    class Input:
        title = graphene.String(required=True)
        body = graphene.String(required=True)
        received_benefit = graphene.String()
        provided_benefit = graphene.String()
        our_participants = graphene.String()
        other_participants = graphene.String()
        date = DateTime(required=True)
        is_draft = graphene.Boolean(default_value=False)

    report = graphene.Field(types.Report)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if not info.context.user.is_authenticated:
            raise Exception('User must be logged in to perform this mutation.')

        author = info.context.user

        report = Report.objects.create(
            author=author,
            date=input.get('date'),
            title=strip_all_tags(input.get('title', '')),
            body=strip_all_tags(input.get('body', '')),
            received_benefit=strip_all_tags(input.get('received_benefit', '')),
            provided_benefit=strip_all_tags(input.get('provided_benefit', '')),
            our_participants=strip_all_tags(input.get('our_participants', '')),
            other_participants=strip_all_tags(input.get('other_participants', '')),
            is_draft=input.get('is_draft'),
        )

        return CreateReport(report=types.Report.from_db(report))


class UpdateReport(relay.ClientIDMutation):

    class Input:
        id = graphene.ID(required=True)
        title = graphene.String(required=True)
        body = graphene.String(required=True)
        received_benefit = graphene.String()
        provided_benefit = graphene.String()
        our_participants = graphene.String()
        other_participants = graphene.String()
        date = DateTime(required=True)
        is_draft = graphene.Boolean(default_value=False)

    report = graphene.Field(types.Report)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if not info.context.user.is_authenticated:
            raise Exception('User must be logged in to perform this mutation.')

        author = info.context.user
        type, id = from_global_id(input.get('id'))

        try:
            report = Report.objects.select_related('author').get(id=id, author_id=author.id)
        except Report.DoesNotExist:
            raise Exception('Viewer is not the Author of this Report or Report does not exist.')

        is_draft = input.get('is_draft')

        if is_draft and not report.is_draft:
            raise Exception('You cannot update published Report with draft.')

        # TODO updating published report older than like a hour should create
        # new revision in history of report

        report.published = arrow.utcnow().datetime
        report.date = input.get('date')
        report.title = strip_all_tags(input.get('title', ''))
        report.body = strip_all_tags(input.get('body', ''))
        report.received_benefit = strip_all_tags(input.get('received_benefit', ''))
        report.provided_benefit = strip_all_tags(input.get('provided_benefit', ''))
        report.our_participants = strip_all_tags(input.get('our_participants', ''))
        report.other_participants = strip_all_tags(input.get('other_participants', ''))
        report.is_draft = is_draft
        report.save()

        return UpdateReport(report=types.Report.from_db(report))


class Mutation:
    login = Login.Field()
    login_by_shortcut = LoginByShortcut.Field()
    # TODO
    # logout = Logout.Field()
    create_report = CreateReport.Field()
    update_report = UpdateReport.Field()
