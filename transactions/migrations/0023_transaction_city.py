# Generated by Django 3.0.5 on 2020-04-30 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0022_auto_20200419_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
