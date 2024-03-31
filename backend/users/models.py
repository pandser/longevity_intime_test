
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='email',
    )
    otp = models.CharField(
        max_length=settings.OTP_LENGTH,
        blank=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
