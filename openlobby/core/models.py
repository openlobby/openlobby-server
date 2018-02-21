from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
import time


class User(AbstractUser):
    """Custom user model. For simplicity we store OpenID 'sub' identifier in
    username field.
    """
    openid_uid = models.CharField(max_length=255, null=True)
    extra = JSONField(null=True, blank=True)
    is_author = models.BooleanField(default=False)
    name_collision_id = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # deal with first name and last name collisions
        collisions = User.objects.filter(first_name=self.first_name, last_name=self.last_name)\
            .order_by('-name_collision_id')
        if len(collisions) > 0 and self not in collisions:
            self.name_collision_id = collisions[0].name_collision_id + 1
        # TODO when we allow name change, it should also reset name_collision_id
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        User.objects.filter(id=self.author.id).update(is_author=True)
