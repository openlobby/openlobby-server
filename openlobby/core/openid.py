from django.conf import settings
from oic.oic import Client
from oic.oic.message import (
    ProviderConfigurationResponse,
    RegistrationResponse,
    ClaimsRequest,
    Claims,
)
from oic.utils.authn.client import CLIENT_AUTHN_METHOD


def init_client_for_uid(openid_uid):
    client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
    issuer = client.discover(openid_uid)
    client.provider_config(issuer)
    return client


def init_client_for_shortcut(openid_client_obj, redirect_uri):
    client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
    set_registration_info(client, openid_client_obj.client_id,
            openid_client_obj.client_secret, redirect_uri)
    info = {
        'issuer': openid_client_obj.issuer,
        'authorization_endpoint': openid_client_obj.authorization_endpoint,
        'token_endpoint': openid_client_obj.token_endpoint,
        'userinfo_endpoint': openid_client_obj.userinfo_endpoint,
    }
    client.provider_info = ProviderConfigurationResponse(**info)
    return client


def register_client(client, redirect_uri):
    params = {
        'redirect_uris': [redirect_uri],
        'client_name': settings.SITE_NAME,
    }
    client.register(client.provider_info['registration_endpoint'], **params)
    return client


def get_authorization_url(client, state):
    args = {
        'client_id': client.client_id,
        'response_type': 'code',
        'scope': ['openid'],
        'state': state,
        'redirect_uri': client.registration_response['redirect_uris'][0],
        'claims': ClaimsRequest(userinfo=Claims(
            name={'essential': True},
            email={'essential': True},
        )),
    }

    auth_req = client.construct_AuthorizationRequest(request_args=args)
    url = auth_req.request(client.provider_info['authorization_endpoint'])
    return url


def set_registration_info(client, client_id, client_secret, redirect_uri):
    info = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uris': [redirect_uri],
    }
    client_reg = RegistrationResponse(**info)
    client.store_registration_info(client_reg)
    return client


def do_access_token_request(client, code, state):
    args = {
        'code': code,
        'client_id': client.client_id,
        'client_secret': client.client_secret,
        'redirect_uri': client.registration_response['redirect_uris'][0],
    }
    client.do_access_token_request(state=state, request_args=args)
