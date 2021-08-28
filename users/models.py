from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models



class Role(models.TextChoices):
    MANAGER = 'начальник'
    ENGENEER = 'инженер'
    EMPLOYEE = 'рабочий'
    GUEST = 'гость'


class User(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True
    )
    email = models.EmailField(
        max_length=60,
        unique=True,
        null=True,
        blank=True
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.GUEST
    )
    password = models.CharField(max_length=20, null=True)

    class Meta:
        ordering = ('last_name',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.get_full_name()

    @property
    def is_admin(self):
        return self.is_superuser or self.role == Role.MANAGER

    @property
    def is_moderator(self):
        return self.is_staff or self.role == Role.ENGENEER
