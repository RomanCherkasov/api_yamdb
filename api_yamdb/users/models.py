from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(
        'Роль',
        max_length=16,
        null=False,
        default='user',
        choices=CHOICES,
    )
    bio = models.TextField(
        'Биография',
        null=False,
        default='Без биографии'
    )
