
import json

from django.contrib.auth import get_user_model
from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
User = get_user_model()

class EventOpinion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_opioner')
    event_post = models.ForeignKey("EventGroup", on_delete=models.CASCADE, related_name='event_post_opnion')
    opinion = models.CharField(max_length=200, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.opinion}"


class EventGroup(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False, related_name='event_of',  blank=False, null=False)
    _id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    image = models.ImageField(upload_to='images/', default='../event_thumbline_yw77uq')
    details = models.TextField()
    members = models.ManyToManyField(User, related_name='member_of')
    opinions = models.ManyToManyField(EventOpinion, related_name='event_user_opinion', blank=True)
    deadline = models.DateField()
    tags = models.CharField(max_length=100)
    create_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    def set_tags(self, array):
        self.tags = json.dumps(array)
    
    def get_tags(self):
        return json.loads(self.tags)


