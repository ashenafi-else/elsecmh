# Generated by Django 2.0 on 2019-01-24 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elsecmh', '0018_mat_impl_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialrevision',
            name='camera',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='materialasset',
            name='asset_type',
            field=models.CharField(choices=[('MODEL_ASSET', 'Model asset'), ('AXF_ASSET', 'AxF asset'), ('ENVIRONMENT_ASSET', 'Environment asset'), ('ENVIRONMENT_ASSET', 'Settings asset')], max_length=255, null=True),
        ),
    ]
