"""
    Used to manage Users Account
"""
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):

    username = None
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.CharField("Email", max_length=80, unique=True)
    password = models.CharField("Password", max_length=100)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return str(self.email)
