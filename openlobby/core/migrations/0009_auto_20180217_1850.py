# Generated by Django 2.0.2 on 2018-02-17 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0008_loginattempt_openid_uid")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="openid_uid",
            field=models.CharField(max_length=255, null=True),
        )
    ]
