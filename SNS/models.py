from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class CustomUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=200)
    followers = models.ManyToManyField("self")
    likes = models.ManyToManyField("SNS.Post", related_name="likes")
    reposts = models.ManyToManyField("SNS.Post", related_name="reposts")
    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey("SNS.CustomUser",
                               on_delete=models.CASCADE, related_name="posts")
    text = models.TextField(max_length=170)
    pub_date = models.DateTimeField(default=timezone.now)
    #likes = models.IntegerField(default=0)
    def __str__(self):
        return self.author
