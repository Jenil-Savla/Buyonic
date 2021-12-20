from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser

class MyUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)



class MyUser(AbstractUser):
    username = None

    email = models.EmailField(("Email Address"),primary_key=True)
    name = models.CharField(max_length=25)
    contact = models.BigIntegerField(unique = True,null = True)
    address = models.TextField(max_length = 100, null=True)
    city = models.CharField(max_length=25,null = True)
    state = models.CharField(max_length=25, null = True)

    refund_balance = models.IntegerField(default = 0)
    is_verified = models.BooleanField(default = False)

    is_manufacturer = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    objects = MyUserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        token = Token.objects.get(user=MyUser.objects.get(self.id))
        return token