from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.db.models import Q

from .models import CustomUser, Post
from .forms import RegisterForm


class HomeView(ListView):
    model = Post
    template_name = "SNS/home.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            myFollowers = self.request.user.customuser.followers.all()
            reposts = self.request.user.customuser.reposts.all()
            return Post.objects.filter(Q(author__in=myFollowers) |
                                       Q(pk__in=reposts)).order_by("-pub_date")
        else:
            return super().get_queryset()


class UserListView(ListView):
    model = CustomUser
    template_name = "SNS/user_list.html"
    context_object_name = "customuser_list"


class MyLikeListView(ListView):
    template_name = "SNS/my_like_list.html"
    context_object_name = "my_like_list"

    def get_queryset(self):
        return self.request.user.customuser.likes.all()


class UserPostView(ListView):
    template_name = "SNS/user_post.html"
    context_object_name = "post_list"

    def get_queryset(self):
        self.customuser = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        return Post.objects.filter(author=self.customuser)


class PostDetailView(DetailView):
    model = Post
    template_name = "SNS/post_detail.html"


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        CustomUser(user=user, bio="No bio yet.").save()
        login(self.request, user)
        return response


class PostCreateView(CreateView):
    model = Post
    template_name = "SNS/post_create.html"
    fields = ["text"]
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user.customuser
        return super().form_valid(form)


def add_follower(request, pk):
    user = get_object_or_404(User, pk=pk)
    userInfo = request.user
    userInfo.customuser.followers.add(user.customuser)
    userInfo.save()
    return redirect('user_list')


def delete_follower(request, pk):
    user = get_object_or_404(User, pk=pk)
    userInfo = request.user
    userInfo.customuser.followers.remove(user.customuser)
    userInfo.save()
    return redirect('user_list')


def add_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    userInfo = request.user
    userInfo.customuser.likes.add(post)
    userInfo.save()
    return redirect("home")


def remove_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    userInfo = request.user
    userInfo.customuser.likes.remove(post)
    userInfo.save()
    return redirect("home")


def add_repost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    userInfo = request.user
    userInfo.customuser.reposts.add(post)
    userInfo.save()
    return redirect("home")


def remove_repost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    userInfo = request.user
    userInfo.customuser.reposts.remove(post)
    userInfo.save()
    return redirect("home")
