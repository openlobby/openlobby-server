# Generated by Django 2.0.2 on 2018-02-09 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("core", "0006_auto_20180208_1544")]

    operations = [
        migrations.RemoveField(
            model_name="openidclient", name="authorization_endpoint"
        ),
        migrations.RemoveField(model_name="openidclient", name="token_endpoint"),
        migrations.RemoveField(model_name="openidclient", name="userinfo_endpoint"),
    ]
