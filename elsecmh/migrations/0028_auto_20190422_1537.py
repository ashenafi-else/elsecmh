# Generated by Django 2.1.7 on 2019-04-22 15:37

from django.db import (
    models,
    migrations,
)


class Migration(migrations.Migration):

    dependencies = [
        ('elsecmh', '0027_auto_20190402_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialasset',
            name='asset_type',
            field=models.CharField(
                choices=[
                    ('MODEL_ASSET',
                     'Model asset'),
                    ('ENVIRONMENT_ASSET',
                     'Environment asset'),
                    ('SETTINGS_ASSET',
                     'Settings asset'),
                    ('AXF_ASSET',
                     'AxF asset'),
                    ('U3M_ASSET',
                     'U3M asset'),
                    ('PREVIEW_ASSET',
                     'Preview asset')],
                max_length=255,
                null=True),
        ),
    ]
