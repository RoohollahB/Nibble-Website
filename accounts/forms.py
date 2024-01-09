from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import User
from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate, login


class registerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']
        error_messages={
            'email':{
            'unique': 'User with this Email already exists.'
            }
        }

class loginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput)
