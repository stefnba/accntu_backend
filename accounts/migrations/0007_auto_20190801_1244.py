# Generated by Django 2.1.5 on 2019-08-01 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_provider'),
    ]

    operations = [
        migrations.RenameField(
            model_name='provider',
            old_name='field_map',
            new_name='parser_map',
        ),
    ]