from django.shortcuts import redirect
from django.views import View
from django.views.generic.base import TemplateView
import time
import urllib.parse

from .auth import create_access_token
from .models import LoginAttempt, User
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
        state = request.GET.get('state')
        la = LoginAttempt.objects.select_related('openid_client').get(state=state)
        app_redirect_uri = la.app_redirect_uri

        if la.expiration < time.time():
            # TODO redirect to app_redirect_uri with fail
            raise NotImplementedError

        # delete login attempt so it can be used just once
        # TODO delete breaks it with LoginAttempt.DoesNotExist exception, why?!
        # la.delete()

        client = init_client_for_shortcut(la.openid_client)
        user_info = get_user_info(client, query_string)

        user, created = User.objects.get_or_create(username=user_info['sub'], defaults={
            'username': user_info['sub'],
            'first_name': user_info['given_name'],
            'last_name': user_info['family_name'],
            'email': user_info['email'],
            'openid_uid': la.openid_uid,
        })

        token = create_access_token(user.username)
        token_qs = urllib.parse.urlencode({'token': token})
        return redirect('{}?{}'.format(app_redirect_uri, token_qs))
