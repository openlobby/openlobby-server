from django.urls import path, re_path
from graphene_django.views import GraphQLView

from openlobby.core.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    re_path(r'^graphql', GraphQLView.as_view(graphiql=True)),
]
