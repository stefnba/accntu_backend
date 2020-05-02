# Generated by Django 3.0.5 on 2020-04-25 19:47

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_token_data_expires_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='token_data',
            name='token_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={'1': 2}),
            preserve_default=False,
        ),
    ]
