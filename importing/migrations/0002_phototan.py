# Generated by Django 2.2.4 on 2019-08-16 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import importing.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20190814_1802'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('importing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoTAN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('photo_tan', models.ImageField(upload_to=importing.models.get_image_path)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Account')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
