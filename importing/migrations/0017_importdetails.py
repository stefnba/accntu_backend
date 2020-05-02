# Generated by Django 3.0.5 on 2020-04-30 22:51

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importing', '0016_auto_20200430_2123'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file_type', models.CharField(blank=True, choices=[('xls', 'XLS'), ('csv', 'CSV')], max_length=10, null=True)),
                ('csv_sep', models.CharField(blank=True, choices=[(',', ','), (';', ';')], max_length=1, null=True)),
                ('skiprows', models.IntegerField(default=0)),
                ('cutrows', models.IntegerField(default=0)),
                ('file_encoding', models.CharField(blank=True, max_length=10, null=True)),
                ('cols_to_drop', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), blank=True, null=True, size=None)),
                ('date_col', models.CharField(blank=True, max_length=255, null=True)),
                ('date_format', models.CharField(blank=True, choices=[('%d.%m.%Y', '%d.%m.%Y'), ('%d.%m.%y', '11.03.20'), ('timestamp_ms', 'timestamp_ms'), ('timestamp', 'timestamp')], max_length=255, null=True)),
                ('title_col', models.CharField(blank=True, max_length=255, null=True)),
                ('title_fallback_col', models.CharField(blank=True, max_length=255, null=True)),
                ('country_col', models.CharField(blank=True, max_length=255, null=True)),
                ('city_col', models.CharField(blank=True, max_length=255, null=True)),
                ('status_col', models.CharField(blank=True, max_length=255, null=True)),
                ('status_col_map', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('account_amount_col_has_status', models.BooleanField(default=False)),
                ('account_currency_default', models.CharField(blank=True, max_length=255, null=True)),
                ('account_currency_col', models.CharField(blank=True, max_length=255, null=True)),
                ('account_amount_col_has_currency', models.BooleanField(default=False)),
                ('spending_currency_col', models.CharField(blank=True, max_length=255, null=True)),
                ('spending_amount_col_has_currency', models.BooleanField(default=False)),
                ('spending_currency_fallback_to_account_currency', models.BooleanField(default=False)),
                ('account_amount_col', models.CharField(blank=True, max_length=255, null=True)),
                ('account_amount_thousand_sep', models.CharField(blank=True, choices=[('.', '.'), (',', ','), ("'", "'")], max_length=1, null=True)),
                ('account_amount_decimal_sep', models.CharField(blank=True, choices=[('.', '.'), (',', ','), ("'", "'")], max_length=1, null=True)),
                ('spending_amount_col', models.CharField(blank=True, max_length=255, null=True)),
                ('spending_amount_fallback_to_account_amount', models.BooleanField(default=False)),
                ('spending_amount_thousand_sep', models.CharField(blank=True, choices=[('.', '.'), (',', ','), ("'", "'")], max_length=1, null=True)),
                ('spending_amount_decimal_sep', models.CharField(blank=True, choices=[('.', '.'), (',', ','), ("'", "'")], max_length=1, null=True)),
                ('iban_col', models.CharField(blank=True, max_length=255, null=True)),
                ('bic_col', models.CharField(blank=True, max_length=255, null=True)),
                ('reference_text_col', models.CharField(blank=True, max_length=255, null=True)),
                ('reference_text_fallback_col', models.CharField(blank=True, max_length=255, null=True)),
                ('counterparty_col', models.CharField(blank=True, max_length=255, null=True)),
                ('counterparty_fallback_col', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'CSV XLS Import Details',
                'verbose_name_plural': 'CSV XLS Import Details',
                'ordering': ['name'],
            },
        ),
    ]