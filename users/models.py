# from apk.models import Department
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

User = get_user_model()


class Role(models.TextChoices):
    MANAGER = 'начальник'
    ENGENEER = 'инженер'
    EMPLOYEE = 'рабочий'
    GUEST = 'гость'


class Department(models.Model):
    title = models.CharField('название службы', max_length=50,)

    class Meta:
        ordering = ('title',)
        verbose_name = 'служба филиала'
        verbose_name_plural = 'службы филиала'

    def __str__(self) -> str:
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patronymic = models.CharField(
        'Отчество',
        max_length=50,
        blank=True,
        null=True,
    )
    job_position = models.TextField('Должность', blank=True, null=True)
    role = models.CharField(
        'Права',
        max_length=30,
        choices=Role.choices,
        default=Role.GUEST,
    )
    department = models.ForeignKey(
        Department,
        verbose_name='Место работы',
        on_delete=SET_NULL,
        related_name='user_department',
        null=True,
    )

    @property
    def is_manager(self):
        return self.is_superuser or self.role == Role.MANAGER

    @property
    def is_engeneer(self):
        return self.is_staff or self.role == Role.ENGENEER

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    class Meta:
        ordering = ('user',)
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователей'

    def __str__(self) -> str:
        return self.user.get_full_name()
