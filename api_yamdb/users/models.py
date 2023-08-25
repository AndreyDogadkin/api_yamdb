from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    role = models.CharField(choices=ROLE_CHOICES, default='user')
    bio = models.TextField(verbose_name='Биография', blank=True)
    confirmation_code = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)