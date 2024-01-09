from django.http.response import HttpResponse as HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic import View, TemplateView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User, Token
from django.urls import reverse_lazy
from .forms import registerForm, loginForm
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .utils import send_token_email
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class HomeView(TemplateView):
    template_name = 'home.html'

def SendActivationMailView(request, email):
    user = User.objects.get(email=email)
    if user.is_verified:
        return HttpResponse('Your email already verified.')
    send_token_email(scheme=request.scheme, host=request.get_host(), email=email, type='activation')
    return HttpResponse('activation link is succesfully send...')


def activate_account(request, uid, token):
    try:
        id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=id)
        t = Token.objects.get(token_key=token)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, Token.DoesNotExist):
        return HttpResponse("Activation link is invalid.")
    
    if user.is_verified:
        return HttpResponse('Your email already verified.')
    
    if not t.is_valid:
        send_again = reverse_lazy('send-activation', kwargs={'email': user.email})
        return HttpResponse('Your link has expired!<br>click on the link to send again: ' + send_again)
    
    if t.user.email == user.email:
        user.is_verified = True
        user.save()
        return HttpResponse("Your account has been activated successfully!")
    else:
        return HttpResponse("Activation link is invalid.")
    
class registerView(CreateView):
    model = User
    form_class = registerForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class LoginView(View):
    form_class = loginForm
    template_name = 'accounts/login.html'
    success_url = '/admin/'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
        
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_verified:
                    login(request, user)
                    messages.success(request, 'you logged in successfully')
                    return redirect('home')
                else:
                    verification_link = reverse_lazy('send-activation', kwargs={'email': user.email})
                    messages.error(request, 'please verify your email...<br>'+verification_link)
            else:
                messages.error(request, 'username or password is wrong.', 'warning')
        return render(request, self.template_name, {'form': form})
    
class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully')
        return redirect('home')
