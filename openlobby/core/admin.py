from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import OpenIdClient, User


@admin.register(OpenIdClient)
class OpenIdClientAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class MyUserAdmin(UserAdmin):
    pass
