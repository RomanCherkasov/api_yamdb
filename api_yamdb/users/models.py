from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True
    )
    password = models.CharField(
        'password',
        max_length=128,
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=128,
        blank=False,
        default='user',
    )
