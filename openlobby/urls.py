from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from openlobby.core.views import IndexView, LoginRedirectView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login-redirect', LoginRedirectView.as_view(), name='login-redirect'),
    path('admin/', admin.site.urls),
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
