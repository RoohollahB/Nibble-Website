from django.views.generic.edit import CreateView
from django.views.generic import View, TemplateView
from django.shortcuts import render, redirect
from .models import User
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


class IndexView(TemplateView):
    template_name = 'home.html'


class RegisterView(CreateView):
    form_class = RegisterForm
    model = User
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            super(RegisterView, self).form_valid(form)
            SendActivationEmailView(request, form.cleaned_data['email'])
            return redirect('login')
        return render(request, self.template_name, {'form': form})


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
                if user.is_verified:
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


def ActivateAccountView(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, 'Your account has been activated! Now you can login')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid')

    return redirect('login')

def SendActivationEmailView(request, email):
    user = User.objects.get(email=email)
    subject = 'Activate your account.'
    message = render_to_string('accounts/template_active_account.html', {
        'name': user.name,
        'protocol': request.scheme,
        'domain': request.get_host(),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)
    })
    email = EmailMessage(subject, message, to=[email,])
    if email.send():
        messages.success(request, f'Dear <b>{user.name}</b>, please go to you email <b>{email}</b> inbox and click on \
                   received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {email}, check if you typed it correctly.')
