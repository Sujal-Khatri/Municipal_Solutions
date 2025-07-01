from django.db import models
from accounts.models import CustomUser

class DiscussionPost(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='discussion_images/', blank=True, null=True)  # NEW
    location = models.CharField(max_length=255, blank=True, null=True)  # For storing map location
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title