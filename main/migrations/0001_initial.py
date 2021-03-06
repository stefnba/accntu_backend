# Generated by Django 2.1.5 on 2019-02-10 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('title_original', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('spending_amount', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('spending_curr', models.CharField(max_length=3)),
                ('spending_account_rate', models.DecimalField(decimal_places=4, max_digits=1000)),
                ('account_amount', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('account_curr', models.CharField(max_length=3)),
                ('account_user_rate', models.DecimalField(decimal_places=4, max_digits=1000)),
                ('user_amount', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('user_curr', models.CharField(max_length=3)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date', 'created_at'],
            },
        ),
    ]
