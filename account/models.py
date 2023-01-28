from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

# Create your models here.
User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='images/', default='../sample_vwadx7')
    username=models.CharField(max_length=40,unique=True)
    email=models.CharField(max_length=80,unique=True)
    phone_number=PhoneNumberField(unique=True, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name}'s Profile"

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance , full_name=f"{instance.first_name} {instance.last_name}",  username = instance.username, email = instance.email, phone_number = instance.phone_number)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


