# Generated by Django 2.2.4 on 2019-09-08 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0011_icon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='icon',
            old_name='title',
            new_name='name',
        ),
    ]