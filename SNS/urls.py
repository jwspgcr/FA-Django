from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('userlist', views.UserListView.as_view(), name='user_list'),
    path('follow/<int:pk>', views.add_follower, name='follow'),
    path('unfollow/<int:pk>', views.delete_follower, name='unfollow'),
    path('user/<int:pk>',views.UserPostView.as_view(),name='user_post'),
    path('like/<int:pk>',views.add_like,name='add_like'),
    path('likes',views.MyLikeListView.as_view(),name='my_like_list'),
    path('unlike/<int:pk>',views.remove_like,name='remove_like'),
    path('repost/<int:pk>',views.add_repost,name='add_repost'),
    path('unrepost/<int:pk>',views.remove_repost,name='remove_repost'),
    path('post/detail/<int:pk>',views.PostDetailView.as_view(),name='post_detail'),
]
