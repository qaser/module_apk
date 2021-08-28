from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Location(models.Model):
    pass


class Act(models.Model):
    year = models.IntegerField(
        'год регистрации акта'
    )
    number = models.PositiveSmallIntegerField('номер акта',)
    compile_data = models.DateField('дата составления', auto_now_add=True)


class Fault(models.Model):
    LEVEL = (
        ('first', 'Первый уровень'),
        ('second', 'Второй уровень'),
        ('third', 'Третий уровень'),
        ('fourth', 'Четвёртый уровень'),
        ('winter_prepare', 'Подготовка к зиме'),
        ('supervisory', 'Газнадзор'),
        ('audit', 'Аудит')
    )
    GROUP = (
        ('labor safety', 'Охрана труда'),
        ('industrial safety', 'Промышленная безопасность'),
        ('fire safety', 'Пожарная безопасность'),
        ('ecological safety', 'Экологическая безопасность'),
    )
    control_level = models.TextField(
        'группа несоответствий',
        choices=LEVEL,
    )
    group = models.TextField(
        'уровень проверки',
        choices=GROUP,
    )
    act = models.ForeignKey(
        Act,
        on_delete=models.SET_NULL,
        verbose_name='номер акта',
        related_name='fault',
        null=True,
        blank=True,
        db_index=True,
    )
    # num_fault = models.PositiveIntegerField()  # номер несоответствия согласно акта
    location = models.TextField('место обнаружения')
    description = models.TextField(
        'описание несоответствия',
        max_length=500,
    )
    document = models.TextField(
        'нормативный документ',
        max_length='150',
    )
    section_esupb = models.TextField(
        'раздел ЕСУПБ',
        max_length='150',
        blank=True,
        null=True,
    )
    inspector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='inspector',
        verbose_name='проверяющий',
        blank=True,
        null=True,
    )
    intruder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='intruder',
        verbose_name='допустивший несоответствие',
        blank=True,
        null=True,
    )
    # control_date = models.DateField(  # может и не надо!!!
    #     'дата проверки',
    #     auto_now_add=True,
    # )
    image_before = models.ImageField(
        'фото несоответствия',
        upload_to='apk/photo_before/',
        blank=True,
        null=True,
    )
    # мероприятия по устранению несоответствия
    fix_action = models.TextField(
        'мероприятие по устранению',
        null=True,
        blank=True,
    )
    fixer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='исполнитель',
        on_delete=models.SET_NULL,
        related_name='fixer',
        null=True,
        blank=True,
    )
    fix_deadline = models.DateField(
        'срок устранения',
        # auto_now_add=True,
        null=True,
        blank=True,
    )
    fixed = models.BooleanField(
        'устранено',
        default=False,
    )
    fix_date = models.DateField(
        'дата устранения несоответствия',
        null=True,
        blank=True,
    )
    image_after = models.ImageField(
        'фото устранения',
        upload_to='apk/photo_after/',
        blank=True,
        null=True,
    )
    # корректирующие действия
    reason = models.TextField()
    correct_action = models.TextField()
    resources = models.TextField()
    corrector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='исполнитель',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    correct_deadline = models.DateField(
        'срок корректировки',
        auto_now_add=True,
    )
    corrected = models.BooleanField(
        'отметка о корректировке',
        default=False,    
    )
    correct_date = models.DateField(
        'дата корректировки',
        null=True,
        blank=True,
    )
