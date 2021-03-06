# Generated by Django 2.2.4 on 2019-08-18 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importing', '0004_auto_20190818_1117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newimport',
            options={'ordering': ['imported_at'], 'verbose_name': 'Import', 'verbose_name_plural': 'Imports'},
        ),
        migrations.AlterModelOptions(
            name='newimportoneaccount',
            options={'ordering': ['imported_at'], 'verbose_name': 'Import per Account', 'verbose_name_plural': 'Imports per Account'},
        ),
        migrations.AddField(
            model_name='newimport',
            name='import_success',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='newimportoneaccount',
            name='import_success',
            field=models.BooleanField(default=False),
        ),
    ]
