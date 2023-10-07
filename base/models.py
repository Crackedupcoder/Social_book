from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True) 
    avatar = models.ImageField(upload_to='avatar',default='forum-author1.png')
    location = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return self.user.username
    

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    caption = models.TextField()
    no_of_likes = models.IntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.caption
    

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    

class FollowerCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
