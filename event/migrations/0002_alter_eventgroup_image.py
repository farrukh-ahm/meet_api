# Generated by Django 4.1.5 on 2023-01-28 12:06

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventgroup',
            name='image',
            field=cloudinary.models.CloudinaryField(default='../event_thumbline_yw77uq', max_length=255, verbose_name='image'),
        ),
    ]
