# Generated by Django 2.1.5 on 2019-05-22 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0011_auto_20190520_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='report',
            name='start_date',
            field=models.DateField(),
        ),
    ]