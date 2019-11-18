# Generated by Django 2.1.7 on 2019-05-16 15:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elsecmh', '0030_auto_20190515_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialasset',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='materialimplementationasset',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, default=list, null=True, size=None),
        ),
    ]
