# Generated by Django 2.1.5 on 2019-05-17 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_auto_20190421_1806'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['updated_at']},
        ),
        migrations.AddField(
            model_name='report',
            name='nmbr_items',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('submitted', 'Submitted')], default='draft', max_length=10),
        ),
        migrations.AddField(
            model_name='report',
            name='sum',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
