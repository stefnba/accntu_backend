# Generated by Django 3.0.5 on 2020-04-05 14:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importing', '0009_auto_20200405_1242'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='csvxlsimportdetails',
            options={'ordering': ['name'], 'verbose_name': 'CSV XLS Import Details', 'verbose_name_plural': 'CSV XLS Import Details'},
        ),
        migrations.AddField(
            model_name='csvxlsimportdetails',
            name='cols_to_drop',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), blank=True, null=True, size=None),
        ),
    ]
