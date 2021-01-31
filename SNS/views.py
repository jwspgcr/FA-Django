from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy

from .models import CustomUser
from .forms import RegisterForm


def home(request):
    return render(request, "SNS/home.html")


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url=reverse_lazy("home")
    def form_valid(self,form):
        # # authenticate(
        # #     username=form.cleaned_data["username"],
        # #     # password=form.cleaned_data["password"]
        # # )
        # username = form.cleaned_data['username']
        # user = User.objects.get(username=username)
        # login(request, user)
        # # return redirect('/')
        # return super().form_valid(form)
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response
