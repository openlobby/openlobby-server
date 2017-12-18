from django.contrib import admin

from .models import OpenIdClient


@admin.register(OpenIdClient)
class OpenIdClientAdmin(admin.ModelAdmin):
    pass
