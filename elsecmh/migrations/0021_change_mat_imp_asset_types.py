# Generated by Django 2.0 on 2019-01-30 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elsecmh', '0020_rename_asset_type_in_mat_rev_asset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialimplementationasset',
            name='asset_type',
            field=models.CharField(choices=[('MODEL_ASSET', 'Model asset'), ('PREVIEW_ASSET', 'Preview asset'), ('JSON_ASSET', 'JSON asset'), ('HTML_ASSET', 'HTML asset')], max_length=255, null=True),
        ),
    ]
