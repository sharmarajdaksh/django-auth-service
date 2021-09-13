from uuid import uuid4
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model

from common.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    username = models.UUIDField(primary_key=True, default=uuid4, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False, blank=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.username)


class BaseToken(models.Model):
    key = models.CharField(max_length=64, default=uuid4, null=False, blank=False)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    expiry_hours = 24

    @property
    def is_token_valid(self) -> bool:
        expiry_datetime = self.created + timedelta(hours=self.expiry_hours)
        return expiry_datetime < datetime.now()
