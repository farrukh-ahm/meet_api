# Generated by Django 4.1.5 on 2023-01-28 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_alter_eventgroup_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventgroup',
            name='image',
            field=models.ImageField(default='../event_thumbline_yw77uq', upload_to='images/'),
        ),
    ]
