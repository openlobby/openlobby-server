from factory import DjangoModelFactory, Faker, SubFactory
from django.conf import settings

from openlobby.core.models import Report


class UserFactory(DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = Faker("user_name")
    first_name = Faker("first_name")
    last_name = Faker("last_name")


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = Faker("user_name")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    is_author = True


class ReportFactory(DjangoModelFactory):
    class Meta:
        model = Report

    author = SubFactory(AuthorFactory)
    date = Faker("past_datetime")
    title = Faker("sentence")
    body = Faker("sentence")
    received_benefit = Faker("word")
    provided_benefit = Faker("word")
    our_participants = Faker("name")
    other_participants = Faker("name")
