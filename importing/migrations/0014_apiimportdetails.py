# Generated by Django 3.0.5 on 2020-04-30 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importing', '0013_upload'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIImportDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date_col', models.CharField(blank=True, max_length=255, null=True)),
                ('date_format', models.CharField(blank=True, choices=[('%d.%m.%Y', '%d.%m.%Y'), ('%d.%m.%y', '11.03.20')], max_length=10, null=True)),
            ],
        ),
    ]