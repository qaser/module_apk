from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE, SET_NULL


class Location(models.Model):
    department = models.TextField(
        'служба',
        max_length=50,
    )
    object = models.TextField(
        'оборудование',
        max_length=100,
    )

    class Meta:
        ordering = ('-department',)
        verbose_name = 'объект проверки'
        verbose_name_plural = 'объекты проверки'

    def __str__(self) -> str:
        return f'{self.department} | {self.object}'


class Act(models.Model):
    LEVEL = (
        ('3 уровень', '3 уровень'),
        ('4 уровень', '4 уровень'),
        ('План подготовки к ОЗП', 'План подготовки к ОЗП')
        ('Газнадзор', 'Газнадзор'),
        ('Аудит', 'Аудит')
    )
    control_level = models.TextField(
        'Уровень проверки',
        choices=LEVEL,
    )
    act_year = models.IntegerField(
        'Год регистрации акта'
    )
    act_number = models.PositiveSmallIntegerField('Номер акта',)
    act_compile_date = models.DateField('Дата составления', auto_now_add=True)

    class Meta:
        ordering = ('-act_compile_date',)
        verbose_name = 'акт'
        verbose_name_plural = 'акты'

    def __str__(self):
        return (
            f'Акт №{self.act_number}-{self.act_year} | {self.control_level}'
        )


class Fault(models.Model):
    GROUP = (
        ('labor safety', 'Охрана труда'),
        ('industrial safety', 'Промышленная безопасность'),
        ('fire safety', 'Пожарная безопасность'),
        ('ecological safety', 'Экологическая безопасность'),
    )
    group = models.TextField(
        'Группа несоответствий',
        choices=GROUP,
    )
    act = models.ForeignKey(
        Act,
        on_delete=SET_NULL,
        verbose_name='Номер акта',
        related_name='fault',
        null=True,
        db_index=True,
    )
    location = models.ForeignKey(
        Location,
        on_delete=CASCADE,
        verbose_name='Место обнаружения',
        related_name='location',
        )
    description = models.TextField(
        'Описание несоответствия',
        max_length=500,
    )
    document = models.TextField(
        'Нормативный документ',
        max_length='150',
    )
    danger = models.BooleanField(
        'Опасное событие?',
        default=False,
    )
    # допустивший несоответствие
    intruder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=SET_NULL,
        related_name='intruder',
        verbose_name='Допустивший несоответствие',
        null=True,
    )
    # не выявивший несоответствие на ниженем уровне
    unseeing = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=SET_NULL,
        related_name='unseeing',
        verbose_name='Не выявивший несоответствие',
        null=True,
    )
    section_esupb = models.TextField(
        'Раздел ЕСУПБ',
        max_length='150',
        blank=True,
        null=True,
    )
    inspector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=SET_NULL,
        related_name='inspector',
        verbose_name='Проверяющий',
        blank=True,
        null=True,
    )
    image_before = models.ImageField(
        'Фото несоответствия',
        upload_to='apk/photo_before/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'несоответствие'
        verbose_name_plural = 'несоответствия'

    def __str__(self):
        complex_note = (f'{self.location} - {self.description[:30]}')
        if len(self.description) > 30:
            return complex_note + '...'
        return complex_note


# мероприятия по устранению несоответствия
class Fix(models.Model):
    act = models.ForeignKey(
        Act,
        on_delete=CASCADE,
        verbose_name='Номер акта',
        related_name='act',
        null=True,
        db_index=True,
    )
    fault = models.ForeignKey(
        Fault,
        on_delete=CASCADE,
        verbose_name='Несоответствие',
        related_name='fault',
    )
    fix_action = models.TextField(
        'Мероприятие по устранению',
        null=True,
        blank=True,
    )
    fixer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Исполнитель',
        on_delete=models.SET_NULL,
        related_name='fixer',
        null=True,
        blank=True,
    )
    fix_deadline = models.DateField(
        'Срок устранения',
        null=True,
        blank=True,
    )
    fixed = models.BooleanField(
        'Отметка об устранении',
        default=False,
    )
    fix_date = models.DateField(
        'Дата устранения несоответствия',
        null=True,
        blank=True,
    )
    image_after = models.ImageField(
        'Фото устранения',
        upload_to='apk/photo_after/',
        blank=True,
        null=True,
    )
    # корректирующие действия
    reason = models.TextField(
        'Причина появления несоответствия',
        max_length=500,
        blank=True,
        null=True,
    )
    correct_action = models.TextField(
        'Коррекция',
    )
    resources = models.TextField(
        'Необходимые ресурсы',
    )
    corrector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Исполнитель',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    correct_deadline = models.DateField(
        'Срок корректировки',
    )
    corrected = models.BooleanField(
        'Отметка о корректировке',
        default=False,    
    )
    correct_date = models.DateField(
        'Дата корректировки',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'мероприятие'
        verbose_name_plural = 'мероприятия'
