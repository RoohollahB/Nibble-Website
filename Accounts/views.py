from django.http.response import HttpResponse as HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic import View, TemplateView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class IndexView(TemplateView):
    template_name = 'home.html'


class RegisterView(CreateView):
    form_class = RegisterForm
    model = User
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)


class LoginView(View):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('admin')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'You logged in successfully!')
                    return redirect('home')
                else:
                    messages.error(request, 'Please verify your email...')
            else:
                messages.error(request, 'username or password is incorrect.')
        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Logged out successfully!')
        return redirect('home')

