# Generated by Django 3.0.5 on 2020-04-30 22:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_auto_20200430_2251'),
    ]

    operations = [
        migrations.RenameField(
            model_name='provider',
            old_name='csvxls_import',
            new_name='import_details',
        ),
        migrations.RemoveField(
            model_name='provider',
            name='api_import',
        ),
    ]
