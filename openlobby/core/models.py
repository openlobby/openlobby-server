import time

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Count
from django.db.models import Q
from django.utils import timezone


class CustomUserManager(UserManager):
    def sorted(self, **kwargs):
        # inline import intentionally
        from openlobby.core.api.schema import (
            AUTHOR_SORT_LAST_NAME_ID,
            AUTHOR_SORT_TOTAL_REPORTS_ID,
        )

        qs = self.get_queryset().annotate(
            total_reports=Count("report", filter=Q(report__is_draft=False))
        )
        sort_field = kwargs.get("sort", AUTHOR_SORT_LAST_NAME_ID)

        if sort_field == AUTHOR_SORT_LAST_NAME_ID:
            return qs.order_by(
                "{}last_name".format("-" if kwargs.get("reversed", False) else ""),
                "first_name",
            )
        elif sort_field == AUTHOR_SORT_TOTAL_REPORTS_ID:
            return qs.order_by(
                "{}total_reports".format("" if kwargs.get("reversed", False) else "-"),
                "last_name",
            )

        raise NotImplementedError("Other sort types are not implemented")


class User(AbstractUser):
    """Custom user model. For simplicity we store OpenID 'sub' identifier in
    username field.
    """

    openid_uid = models.CharField(max_length=255, null=True)
    extra = JSONField(null=True, blank=True)
    is_author = models.BooleanField(default=False)
    has_colliding_name = models.BooleanField(default=False)
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        # deal with first name and last name collisions
        if self.is_author:
            collisions = User.objects.filter(
                first_name=self.first_name, last_name=self.last_name, is_author=True
            ).exclude(id=self.id)
            if collisions.count() > 0:
                self.has_colliding_name = True
                collisions.update(has_colliding_name=True)
        super().save(*args, **kwargs)


class OpenIdClient(models.Model):
    """Stores connection parameters for OpenID Clients. Some may be used as
    login shortcuts.
    """

    name = models.CharField(max_length=255)
    is_shortcut = models.BooleanField(default=False)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name


def get_login_attempt_expiration():
    return int(time.time() + settings.LOGIN_ATTEMPT_EXPIRATION)


class LoginAttempt(models.Model):
    """Temporary login attempt details which persists redirects."""

    openid_client = models.ForeignKey(OpenIdClient, on_delete=models.CASCADE)
    state = models.CharField(max_length=50, unique=True, db_index=True)
    app_redirect_uri = models.CharField(max_length=255)
    openid_uid = models.CharField(max_length=255, null=True)
    expiration = models.IntegerField(default=get_login_attempt_expiration)


class Report(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date = models.DateTimeField()
    published = models.DateTimeField(default=timezone.now)
    title = models.TextField(null=True, blank=True)
    body = models.TextField()
    received_benefit = models.TextField(null=True, blank=True)
    provided_benefit = models.TextField(null=True, blank=True)
    our_participants = models.TextField(null=True, blank=True)
    other_participants = models.TextField(null=True, blank=True)
    extra = JSONField(null=True, blank=True)
    is_draft = models.BooleanField(default=False)
    superseded_by = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    edited = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.is_draft and not self.author.is_author:
            self.author.is_author = True
            self.author.save()
