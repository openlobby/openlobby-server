from django.shortcuts import redirect
from django.views import View
from django.views.generic.base import TemplateView
import time
import urllib.parse

from .models import LoginAttempt
from .openid import (
    init_client_for_shortcut,
    get_user_info,
)


class IndexView(TemplateView):
    template_name = 'core/index.html'


class LoginRedirectView(View):

    # TODO redirect to app_redirect_uri on fail
    def get(self, request, **kwargs):
        query_string = request.META['QUERY_STRING']

        # get login attempt
        state = urllib.parse.parse_qs(query_string)['state'][0]
        la = LoginAttempt.objects.select_related('openid_client').get(state=state)
        app_redirect_uri = la.app_redirect_uri

        # check login attempt expiration
        if la.expiration < time.time():
            # TODO redirect to app_redirect_uri with fail
            raise NotImplementedError

        # delete login attempt so it can be used just once
        # TODO delete breaks it with LoginAttempt.DoesNotExist exception, why?!
        # la.delete()

        # get OpenID user info
        client = init_client_for_shortcut(la.openid_client)
        user_info = get_user_info(client, query_string)
        print('\nUSER INFO:', user_info, '\n')

        # TODO get or create User

        # TODO create session
        # expiration = get_session_expiration_time()

        # TODO create access token for session
        # token = create_access_token(session.meta.id, expiration)

        # TODO add token
        return redirect(app_redirect_uri)
