from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView

from openlobby.core.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('graphql', GraphQLView.as_view(graphiql=True)),
]
