import json
import graphene
from graphene import relay
from oic.oic import rndstr
from oic.oic.message import AuthorizationResponse

from .auth import (
    init_client_for_uid,
    register_client,
    get_authorization_url,
    set_registration_info,
    do_access_token_request,
)


class Login(relay.ClientIDMutation):

    class Input:
        openid_uid = graphene.String(required=True)
        redirect_uri = graphene.String(required=True)

    authorization_url = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        openid_uid = input['openid_uid']
        redirect_uri = input['redirect_uri']

        client = init_client_for_uid(openid_uid)
        client = register_client(client, redirect_uri)

        state = rndstr()
        nonce = rndstr()
        session = {
            'state': state,
            'nonce': nonce,
            'client_id': client.client_id,
            'client_secret': client.client_secret,
            'openid_uid': openid_uid,
            'redirect_uri': redirect_uri,
        }

        # TODO save session in ES
        with open('session.json', 'w') as f:
            f.write(json.dumps(session))

        authorization_url = get_authorization_url(client, state, nonce)

        return Login(authorization_url=authorization_url)


class LoginRedirect(relay.ClientIDMutation):

    class Input:
        query_string = graphene.String(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        query_string = input['query_string']

        with open('session.json', 'r') as f:
            session = json.loads(f.read())

        client = init_client_for_uid(session['openid_uid'])
        client = set_registration_info(client, session['client_id'], session['client_secret'], session['redirect_uri'])

        aresp = client.parse_response(AuthorizationResponse, info=query_string, sformat='urlencoded')

        code = aresp['code']
        state = aresp['state']
        assert state == session['state']

        do_access_token_request(client, code, state)

        user_info = client.do_user_info_request(state=state)

        print('\nLOGIN SUCCESSFUL!', user_info, '\n')

        return LoginRedirect(success=True)


class Mutations(graphene.ObjectType):
    login = Login.Field()
    login_redirect = LoginRedirect.Field()
