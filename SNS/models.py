from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    #username=models.CharField(default=user.Objects.get("username"))
    bio = models.TextField(max_length=200)

    def __str__(self):
        return self.username
