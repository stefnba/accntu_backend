# Generated by Django 3.0.5 on 2020-04-10 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20200405_1719'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sub_account',
            options={'verbose_name': 'Sub-Account', 'verbose_name_plural': 'Sub-Accounts'},
        ),
    ]
