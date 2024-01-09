from django.conf import settings
from django.core.mail import send_mail
from .models import Token, User
import uuid
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.utils import timezone


def send_token_email(scheme, host ,email, type):
    user = User.objects.get(email=email)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # create a token
    token = str(uuid.uuid4())
    expires_at = timezone.now() + timezone.timedelta(minutes=15)
    Token.objects.create(user=user, token_key=token, token_type='activation',expires_at= expires_at)

    # create email content
    if type == 'activation':
        subject = 'Please verify your email address.'
        message = f'Click on the link to verify: {scheme}://{host}/accounts/activate/{uid}/{token}/'
    else: # type == 'reset-password'
        subject = 'Password Reset Link'
        message = f'Click on the link to reset your password: {scheme}://{host}/accounts/reset-password/{uid}/{token}/'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    try:
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        print(e)
    return True
