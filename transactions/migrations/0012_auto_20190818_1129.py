# Generated by Django 2.2.4 on 2019-08-18 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0011_auto_20190815_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='importing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='importing.NewImportOneAccount'),
        ),
    ]