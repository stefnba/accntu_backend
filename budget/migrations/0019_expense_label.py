# Generated by Django 2.2.4 on 2019-09-19 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0018_auto_20190919_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='label',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='label', to='budget.Label'),
        ),
    ]