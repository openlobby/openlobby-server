from django.conf import settings
from oic.oic import Client
from oic.oic.message import (
    RegistrationResponse,
    ClaimsRequest,
    Claims,
)
from oic.utils.authn.client import CLIENT_AUTHN_METHOD


def discover_issuer(openid_uid):
    client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
    return client.discover(openid_uid)


def init_client_for_shortcut(openid_client_obj):
    client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
    reg_info = {
        'client_id': openid_client_obj.client_id,
        'client_secret': openid_client_obj.client_secret,
        'redirect_uris': [settings.REDIRECT_URI],
    }
    client_reg = RegistrationResponse(**reg_info)
    client.store_registration_info(client_reg)
    client.provider_config(openid_client_obj.issuer)
    return client


def register_client(issuer):
    client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
    client.provider_config(issuer)
    params = {
        'redirect_uris': [settings.REDIRECT_URI],
        'client_name': settings.SITE_NAME,
    }
    client.register(client.provider_info['registration_endpoint'], **params)
    return client


def get_authorization_url(client, state):
    args = {
        'client_id': client.client_id,
        'response_type': 'code',
        'scope': 'openid',
        'state': state,
        'redirect_uri': client.registration_response['redirect_uris'][0],
        'claims': ClaimsRequest(userinfo=Claims(
            given_name={'essential': True},
            family_name={'essential': True},
            email={'essential': True},
        )),
    }

    auth_req = client.construct_AuthorizationRequest(request_args=args)
    return auth_req.request(client.provider_info['authorization_endpoint'])


def do_access_token_request(client, code, state):
    args = {'code': code, 'redirect_uri': settings.REDIRECT_URI}
    client.do_access_token_request(state=state, request_args=args)
