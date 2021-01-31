from django import forms
from .models import CustomUser
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)
