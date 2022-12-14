# Generated by Django 4.0.6 on 2022-10-02 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HouseListing', '0025_properties_businesslounge_properties_cctv_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='properties',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='properties',
            name='approved_by_admin',
            field=models.IntegerField(default=0),
        ),
    ]
