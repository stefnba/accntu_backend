# Generated by Django 2.1.5 on 2019-05-19 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0008_auto_20190519_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='nmbr_items',
        ),
        migrations.RemoveField(
            model_name='report',
            name='sum',
        ),
    ]
