# Generated by Django 3.0.5 on 2020-05-14 20:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_auto_20200411_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='add_user_info', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]