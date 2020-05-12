# Generated by Django 3.0.5 on 2020-05-06 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('importing', '0020_auto_20200501_0003'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newimportoneaccount',
            options={'ordering': ['-imported_at'], 'verbose_name': 'Import per Account', 'verbose_name_plural': 'Imports per Account'},
        ),
        migrations.AlterField(
            model_name='newimportoneaccount',
            name='new_import',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='importing.NewImport'),
        ),
    ]
