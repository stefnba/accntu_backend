# Generated by Django 2.1.5 on 2019-05-19 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_transaction_label'),
        ('business', '0006_auto_20190519_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('report_amount', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='transactions.Transaction')),
                ('report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.Report')),
            ],
        ),
    ]
