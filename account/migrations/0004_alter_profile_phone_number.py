# Generated by Django 4.1.5 on 2023-01-28 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_profile_phone_number_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(max_length=80, unique=True, verbose_name='Phone Number'),
        ),
    ]
