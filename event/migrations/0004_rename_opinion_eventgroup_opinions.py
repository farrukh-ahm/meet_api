# Generated by Django 4.1.5 on 2023-02-01 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_alter_eventgroup_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventgroup',
            old_name='opinion',
            new_name='opinions',
        ),
    ]