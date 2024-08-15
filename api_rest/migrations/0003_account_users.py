# Generated by Django 5.1 on 2024-08-15 19:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_rest", "0002_account"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="users",
            field=models.ManyToManyField(
                related_name="accounts", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
