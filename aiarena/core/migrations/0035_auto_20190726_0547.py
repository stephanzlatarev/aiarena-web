# Generated by Django 2.1.7 on 2019-07-25 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_statsbotmatchups_statsbots'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='round',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Round'),
        ),
    ]
