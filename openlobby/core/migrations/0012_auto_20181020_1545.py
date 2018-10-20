# Generated by Django 2.1.2 on 2018-10-20 13:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import openlobby.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_report_is_draft'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', openlobby.core.models.CustomUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='edited',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='report',
            name='superseded_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Report'),
        ),
    ]