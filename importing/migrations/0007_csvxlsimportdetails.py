# Generated by Django 3.0.5 on 2020-04-04 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importing', '0006_newimportoneaccount_new_import'),
    ]

    operations = [
        migrations.CreateModel(
            name='CsvXlsImportDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(blank=True, choices=[('xls', 'XLS'), ('csv', 'CSV')], max_length=10, null=True)),
                ('sep', models.CharField(blank=True, choices=[(',', ','), (';', ';')], max_length=1, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('first_row', models.IntegerField()),
            ],
        ),
    ]