# Generated by Django 4.0.6 on 2022-09-20 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HouseListing', '0018_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='properties',
            name='security_deposit',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='properties',
            name='default_house_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='properties',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
