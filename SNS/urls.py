from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('userlist', views.UserListView.as_view(), name='user_list'),
    path('follow/<int:pk>', views.add_follower, name='follow'),
    path('unfollow/<int:pk>', views.delete_follower, name='unfollow'),
]
