# Generated by Django 3.0.5 on 2020-04-25 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_token_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='token_data',
            name='expires_in',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
