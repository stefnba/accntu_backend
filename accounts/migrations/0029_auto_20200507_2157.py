# Generated by Django 3.0.5 on 2020-05-07 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_auto_20200430_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='first_import_success',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='last_import',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
