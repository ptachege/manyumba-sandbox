# Generated by Django 4.0.6 on 2022-08-25 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HouseListing', '0007_properties_featured_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='properties',
            name='approved_by_admin',
            field=models.BooleanField(default=False),
        ),
    ]
