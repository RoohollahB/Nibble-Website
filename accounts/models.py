from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils import timezone


def get_profile_image_filepath(self, filename):
    return 'profile/profile_images/'+ str(self.pk) + '/profile_image.png'

def get_default_profile_image():
    return 'profile/profile_default/default_profile_image.png'

class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name+ ': ' + self.email

class Address(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    plaque = models.PositiveSmallIntegerField(null=True, blank=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.title is not None:
            return f"{self.user.name.title()} - {self.title.upper()} - {self.street.title()}"
        else:
            return f"{self.user.name.title()} - {self.plaque} - {self.street.title()} - {self.city.title()}"

class Token(models.Model):
    TOKEN_TYPES = (
        ('activation', 'Activation'),
        ('password_reset', 'Password Reset'),
    )

    token_key = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token_type = models.CharField(max_length=20, choices=TOKEN_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return self.expires_at > timezone.now()
    
    def __str__(self):
        return f'{self.user.email} - {self.token_type} - {self.is_valid()}'