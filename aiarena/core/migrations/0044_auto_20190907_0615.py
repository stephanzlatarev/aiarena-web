# Generated by Django 2.1.7 on 2019-09-06 20:45

import aiarena.core.models
import aiarena.core.storage
import aiarena.core.validators
from django.db import migrations
import private_storage.fields

from aiarena.core import models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_auto_20190907_0602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='bot_zip',
            field=private_storage.fields.PrivateFileField(storage=aiarena.core.storage.OverwritePrivateStorage(base_url='/'), upload_to=models.bot.bot_zip_upload_to, validators=[aiarena.core.validators.validate_bot_zip_file]),
        ),
    ]
