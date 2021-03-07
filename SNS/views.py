from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.db.models import Q, F

from .models import CustomUser, Post
from .forms import RegisterForm
from datetime import datetime

def home_view(request):
    user=request.user
    if not user.is_authenticated:
        return render(request, 'SNS/home.html', {'posts': []})
    else:
        myFollowers = user.customuser.followers.all()

        postsNotReposted = Post.objects.filter(
                                    Q(author__in=myFollowers) |
                                    Q(author=user.customuser)
                                    ).exclude(
                                    Q(repost__repostedBy__in=myFollowers)
                                    )

        postsReposted = Post.objects.filter(
                                    Q(repost__repostedBy__in=myFollowers)
                                    ).distinct()
        for p in postsReposted:
            p.keyDate = p.repost_set.latest("pub_date").pub_date
            p.reposter = CustomUser.objects.filter(Q(repost__post=p)).intersection(myFollowers)

        for p in postsNotReposted:
            p.keyDate = p.pub_date

        postsList = list(postsNotReposted)+list(postsReposted)

        contextPosts = sorted(postsList, key=lambda x:x.keyDate, reverse=True)

        return render(request, 'SNS/home.html', {'posts': contextPosts})

@method_decorator(login_required, name="dispatch")
class UserListView(ListView):
    model = CustomUser
    template_name = "SNS/user_list.html"
    context_object_name = "customuser_list"


@method_decorator(login_required, name="dispatch")
class MyLikeListView(ListView):
    template_name = "SNS/my_like_list.html"
    context_object_name = "my_like_list"

    def get_queryset(self):
        return self.request.user.customuser.likes.all()


@method_decorator(login_required, name="dispatch")
class UserPostView(ListView):
    template_name = "SNS/user_post.html"
    context_object_name = "post_list"

    def get_queryset(self):
        self.customuser = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        return Post.objects.filter(author=self.customuser)


@method_decorator(login_required, name="dispatch")
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


@method_decorator(login_required, name="dispatch")
class PostCreateView(CreateView):
    model = Post
    template_name = "SNS/post_create.html"
    fields = ["text"]
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user.customuser
        return super().form_valid(form)

@method_decorator(login_required, name="dispatch")
class ReplyCreateView(CreateView):
    model = Post
    template_name = "SNS/reply_create.html"
    fields = ["text"]
    success_url = reverse_lazy("home")

    def get_context_data(self):
        self.replyTo = get_object_or_404(Post, pk=self.kwargs['pk'])
        context=super().get_context_data()
        context["post"]=self.replyTo
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user.customuser
        form.instance.replyTo = Post.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


@login_required
def add_follower(request, pk):
    user = get_object_or_404(User, pk=pk)
    userInfo = request.user
    userInfo.customuser.followers.add(user.customuser)
    userInfo.save()
    return redirect('user_list')


@login_required
def delete_follower(request, pk):
    user = get_object_or_404(User, pk=pk)
    userInfo = request.user
    userInfo.customuser.followers.remove(user.customuser)
    userInfo.save()
    return redirect('user_list')


@login_required
def add_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    userInfo = request.user
    userInfo.customuser.likes.add(post)
    userInfo.save()
    return redirect("home")


@login_required
def remove_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    userInfo = request.user
    userInfo.customuser.likes.remove(post)
    userInfo.save()
    return redirect("home")


@login_required
def add_repost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    userInfo = request.user
    userInfo.customuser.reposts.add(post)
    userInfo.save()
    return redirect("home")


@login_required
def remove_repost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    userInfo = request.user
    userInfo.customuser.reposts.remove(post)
    userInfo.save()
    return redirect("home")
