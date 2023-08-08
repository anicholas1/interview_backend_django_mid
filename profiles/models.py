from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class UserProfile(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    # Left out several fields since they are inherited from AbstractBaseUser

    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=254, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=254, null=True, blank=True)
    last_name = models.CharField(max_length=254, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField()

    # Same goes here for the property methods such as is_authenticated
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

