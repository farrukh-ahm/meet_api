# Generated by Django 4.1.5 on 2023-01-20 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventGroup',
            fields=[
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=500)),
                ('image', models.ImageField(blank=True, default='default_file/event_thumbline.jpg', null=True, upload_to='event_thumbline')),
                ('details', models.TextField()),
                ('deadline', models.DateField()),
                ('tags', models.CharField(max_length=100)),
                ('create_at', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='event_of', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='member_of', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventOpinion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opinion', models.CharField(max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('event_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_post_opnion', to='event.eventgroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_opioner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='eventgroup',
            name='opinion',
            field=models.ManyToManyField(blank=True, related_name='event_user_opinion', to='event.eventopinion'),
        ),
    ]
