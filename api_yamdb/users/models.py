from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    USER = 1
    MODERATOR = 2
    ADMIN = 3

    ROLE_CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True)
    bio = models.TextField(verbose_name='Биография', blank=True)
    confirmation_code = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)