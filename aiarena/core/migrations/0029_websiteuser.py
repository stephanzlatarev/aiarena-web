# Generated by Django 3.0.14 on 2021-05-05 22:40

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0028_auto_20210419_2336"),
    ]

    operations = [
        migrations.CreateModel(
            name="WebsiteUser",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("single_use_match_requests", models.IntegerField(blank=True, default=0)),
            ],
            options={
                "verbose_name": "WebsiteUser",
            },
            bases=("core.user",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
