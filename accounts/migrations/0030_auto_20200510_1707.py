# Generated by Django 3.0.5 on 2020-05-10 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_auto_20200507_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token_data',
            name='access_token',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='token_data',
            name='host_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='token_data',
            name='refresh_token',
            field=models.TextField(),
        ),
    ]
