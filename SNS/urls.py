from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
]
