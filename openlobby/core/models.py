from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
import time


class User(AbstractUser):
    # TODO remove username, set different login field
    openid_uid = models.CharField(max_length=255, unique=True, db_index=True)
    extra = JSONField(null=True, blank=True)
    is_author = models.BooleanField(default=False)


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        User.objects.filter(id=self.author.id).update(is_author=True)
