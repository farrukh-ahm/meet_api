# Generated by Django 4.1.5 on 2023-01-27 21:00

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=cloudinary.models.CloudinaryField(default='../sample_vwadx7', max_length=255, verbose_name='image'),
        ),
    ]
