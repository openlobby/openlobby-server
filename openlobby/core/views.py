from django.shortcuts import redirect
from django.views import View
from django.views.generic.base import TemplateView
import time
import urllib.parse
from oic.oic.message import AuthorizationResponse

from .models import LoginAttempt
from .openid import (
    init_client_for_shortcut,
    do_access_token_request,
)


class IndexView(TemplateView):
    template_name = 'core/index.html'


class LoginRedirectView(View):

    # TODO redirect to app_redirect_uri on fail
    def get(self, request, **kwargs):
        query_string = request.META['QUERY_STRING']

        # get state from query string
        state = urllib.parse.parse_qs(query_string)['state'][0]

        # get login attempt
        la = LoginAttempt.objects.select_related('openid_client').get(state=state)
        app_redirect_uri = la.app_redirect_uri

        # check login attempt expiration
        if la.expiration < time.time():
            # TODO redirect to app_redirect_uri with fail
            raise NotImplementedError

        # reconstruct OpenID Client
        client = init_client_for_shortcut(la.openid_client)

        # delete login attempt so it can be used just once
        # TODO delete breaks it with LoginAttempt.DoesNotExist exception, why?!
        # la.delete()

        # process query string from OpenID redirect
        aresp = client.parse_response(AuthorizationResponse, info=query_string,
            sformat='urlencoded')
        code = aresp['code']
        assert state == aresp['state']

        # OpenID access token request
        do_access_token_request(client, code, state)

        # OpenID user info request
        user_info = client.do_user_info_request(state=state)
        print('\nUSER INFO:', user_info, '\n')

        # TODO get or create User

        # TODO create session
        # expiration = get_session_expiration_time()

        # TODO create access token for session
        # token = create_access_token(session.meta.id, expiration)

        # TODO add token
        return redirect(app_redirect_uri)
