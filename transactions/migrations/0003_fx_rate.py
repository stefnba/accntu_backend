# Generated by Django 2.1.5 on 2019-03-02 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_fx'),
    ]

    operations = [
        migrations.AddField(
            model_name='fx',
            name='rate',
            field=models.DecimalField(decimal_places=4, default=12, max_digits=1000),
            preserve_default=False,
        ),
    ]