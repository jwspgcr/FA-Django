from django.contrib import admin
from .models import CustomUser, Post, Repost

admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Repost)
