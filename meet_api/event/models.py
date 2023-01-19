from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class EventGroup(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False, related_name='event_of')
    _id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=250, blank=False, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    image = models.ImageField(upload_to='event_thumbline', blank=True, null=True, default='default_file/event_thumbline.jpg')
    members = models.ManyToManyField(User, related_name='member_of')



