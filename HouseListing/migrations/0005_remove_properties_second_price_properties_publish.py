# Generated by Django 4.0.6 on 2022-07-29 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HouseListing', '0004_properties_street'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='properties',
            name='second_price',
        ),
        migrations.AddField(
            model_name='properties',
            name='publish',
            field=models.BooleanField(default=True),
        ),
    ]