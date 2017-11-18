import os
import json
from flask import Flask, redirect, request
from flask_graphql import GraphQLView
from elasticsearch import Elasticsearch
from oic.oic import Client, rndstr
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from oic.oic.message import AuthorizationResponse, RegistrationResponse

from .bootstrap import bootstrap_es
from .schema import schema


app = Flask(__name__)

es_dsn = os.environ.get('ELASTICSEARCH_DSN', 'http://localhost:9200')
es_client = Elasticsearch(es_dsn)

bootstrap_es(es_client)


@app.route('/')
def hello():
    return 'Open Lobby Server\n\nAPI is at: /graphql', 200, {'Content-Type': 'text/plain; charset=utf-8'}


uid = 'janbednarik@mojeid.cz'
redirect_uri = 'http://localhost:8010/redirect'


@app.route('/login')
def login():

    client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
    issuer = client.discover(uid)
    client.provider_config(issuer)

    params = {'redirect_uris': [redirect_uri]}
    client.register(client.provider_info['registration_endpoint'], **params)

    session = {
        'state': rndstr(),
        'nonce': rndstr(),
        'client_id': client.client_id,
        'client_secret': client.client_secret,
    }

    with open('session.json', 'w') as f:
        f.write(json.dumps(session))

    args = {
        'client_id': client.client_id,
        'response_type': 'code',
        'scope': ['openid'],
        'nonce': session['nonce'],
        'redirect_uri': redirect_uri,
        'state': session['state']
    }
    auth_req = client.construct_AuthorizationRequest(request_args=args)
    login_url = auth_req.request(client.authorization_endpoint)

    return redirect(login_url, code=302)


@app.route('/redirect')
def login_redirect():
    with open('session.json', 'r') as f:
        session = json.loads(f.read())

    client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
    issuer = client.discover(uid)
    client.provider_config(issuer)

    info = {
        'client_id': session['client_id'],
        'client_secret': session['client_secret'],
        'redirect_uris': [redirect_uri],
    }
    client_reg = RegistrationResponse(**info)
    client.store_registration_info(client_reg)

    response = request.query_string.decode('utf-8')
    aresp = client.parse_response(AuthorizationResponse, info=response, sformat='urlencoded')

    code = aresp['code']
    assert aresp['state'] == session['state']

    args = {
        'code': code,
        'client_id': client.client_id,
        'client_secret': client.client_secret,
        'redirect_uri': redirect_uri,
    }
    resp = client.do_access_token_request(state=aresp['state'], request_args=args)
    userinfo = client.do_user_info_request(state=aresp['state'])

    return 'OK {}'.format(userinfo)


app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql', schema=schema, graphiql=True, context={'es': es_client}
))
