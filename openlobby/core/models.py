from django.db import models


class OpenIdClient(models.Model):
    """Stores connection parameters for OpenID Clients. Some may be used as
    login shortcuts.
    """
    name = models.CharField(max_length=50)
    is_shortcut = models.BooleanField(default=False)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    authorization_endpoint = models.CharField(max_length=255)
    token_endpoint = models.CharField(max_length=255)
    userinfo_endpoint = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class LoginAttempt(models.Model):
    openid_client = models.ForeignKey(OpenIdClient, on_delete=models.CASCADE)
    state = models.CharField(max_length=50, unique=True, db_index=True)
    redirect_uri = models.CharField(max_length=255)
    expiration = models.IntegerField()
