from django.contrib.auth.models import AbstractUser
from django.db import models


class GramUser(AbstractUser):
    description = models.TextField(max_length=300)
    profile_photo = models.ImageField(upload_to='profile_images/', default='../static/defaultuserimage.png')
    subscribers = models.TextField(default=[])
    subscriptions = models.TextField(default=[])


class Images(models.Model):
    user = models.ForeignKey(GramUser, on_delete=models.CASCADE)
    path = models.TextField()
    name = models.TextField()
    description = models.TextField(max_length=300)
