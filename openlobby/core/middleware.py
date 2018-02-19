import re

from .api.utils import graphql_error_response
from .auth import parse_access_token
from .models import User


class TokenAuthMiddleware:
    """Custom authentication middleware which using JWT token."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header is not None:
            m = re.match(r'Bearer (?P<token>.+)', auth_header)
            if m:
                token = m.group('token')
            else:
                return graphql_error_response('Wrong Authorization header. Expected: "Bearer <token>"')

            try:
                username = parse_access_token(token)
            except Exception:
                return graphql_error_response('Invalid Token.', 401)

            try:
                request.user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass

        return self.get_response(request)
