# Generated by Django 3.0.5 on 2020-04-30 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importing', '0017_importdetails'),
        ('accounts', '0027_auto_20200430_2251'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CsvXlsImportDetails',
        ),
        migrations.AlterField(
            model_name='apiimportdetails',
            name='date_format',
            field=models.CharField(blank=True, choices=[('%d.%m.%Y', '%d.%m.%Y'), ('%d.%m.%y', '11.03.20'), ('timestamp_ms', 'timestamp_ms'), ('timestamp', 'timestamp')], max_length=25, null=True),
        ),
    ]