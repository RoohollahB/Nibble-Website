from email.policy import default
from enum import unique
from tkinter import Widget
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from .manager import UserManager


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
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email


