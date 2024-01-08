from operator import truediv
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, name=None, **extra_fields):
        if not email:
            raise  ValueError('Email is required')
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password=None, name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            name=name,
            **extra_fields
        )
        user.save(using=self.db)
        return user