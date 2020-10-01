from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)

from phonenumber_field.modelfields import PhoneNumberField
from user.user_manager import UserManager

# Create your models here.
#aumentamos el tama;o de password a 80
#agregamos la variable de salt
class User(AbstractBaseUser, PermissionsMixin):
    phone = PhoneNumberField(unique=True)
    is_admin = models.BooleanField(default=False)
    address_a = models.CharField(max_length=45)
    address_b = models.CharField(max_length=45)
    password = models.CharField(max_length=80)
    salt = models.CharField(max_length=80)
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    username = models.CharField(max_length=30, blank=True, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self
