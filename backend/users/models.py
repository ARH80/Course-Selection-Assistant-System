from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email_verified = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, default='M')

    class Meta:
        verbose_name = 'دانشجو'
        verbose_name_plural = 'دانشجویان'

    def __str__(self):
        return self.username