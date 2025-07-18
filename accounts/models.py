from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    is_admin     = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    address      = models.TextField(blank=True)
    email        = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user     = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username}’s profile"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, **kwargs):
    profile, created = Profile.objects.get_or_create(user=instance)
    profile.save()
