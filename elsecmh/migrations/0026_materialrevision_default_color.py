# Generated by Django 2.0 on 2019-03-05 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elsecmh', '0025_add_brand_color_and_color_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialrevision',
            name='default_color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='elsecmh.Color'),
        ),
    ]
