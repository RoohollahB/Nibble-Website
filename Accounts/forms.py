from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']
        error_messages = {
            'email': {
                'unique': 'User with this Email already exists.'
            }
        }


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput)
