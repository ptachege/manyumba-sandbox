# Generated by Django 4.0.6 on 2022-08-25 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HouseListing', '0006_alter_properties_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='properties',
            name='featured_image',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
