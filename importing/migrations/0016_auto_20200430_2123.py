# Generated by Django 3.0.5 on 2020-04-30 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importing', '0015_auto_20200430_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='apiimportdetails',
            name='city_col',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='apiimportdetails',
            name='counterparty_fallback_col',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='apiimportdetails',
            name='country_col',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='apiimportdetails',
            name='title_fallback_col',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
