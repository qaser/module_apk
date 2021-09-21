import datetime as dt

from django.contrib.auth import get_user_model
# from users.models import Profile
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
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


class Location(models.Model):
    department = models.ForeignKey(
        Department,
        verbose_name='служба',
        related_name='department',
        on_delete=CASCADE,
    )
    object = models.CharField(
        'оборудование',
        max_length=100,
    )

    class Meta:
        ordering = ('-department',)
        verbose_name = 'объект проверки'
        verbose_name_plural = 'объекты проверки'

    def __str__(self) -> str:
        return f'{self.department} | {self.object}'


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


class Act(models.Model):
    LEVEL = (
        ('3 уровень', '3 уровень'),
        ('4 уровень', '4 уровень'),
        ('План подготовки к ОЗП', 'План подготовки к ОЗП'),
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
    closed = models.BooleanField('Отработан', default=False)

    class Meta:
        ordering = ('-act_compile_date',)
        verbose_name = 'акт'
        verbose_name_plural = 'акты'
        constraints = [
            models.UniqueConstraint(
                fields=['act_year', 'act_number'],
                name='unique_act_numbering'
            ),
        ]

    def __str__(self):
        return (
            f'Акт №{self.act_number}-{self.act_year} | {self.control_level}'
        )


class Fault(models.Model):
    GROUP = (
        ('ОТ', 'Охрана труда'),
        ('ПБ', 'Промышленная безопасность'),
        ('ПОЖ', 'Пожарная безопасность'),
        ('Э', 'Экологическая безопасность'),
    )
    fault_number = models.PositiveIntegerField('Номер несоответствия')
    group = models.TextField(
        'Группа несоответствий',
        choices=GROUP,
    )
    act = models.ForeignKey(
        Act,
        on_delete=SET_NULL,
        verbose_name='Номер акта',
        related_name='faults',
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
    document = models.CharField(
        'Нормативный документ',
        max_length=100,
    )
    danger = models.BooleanField(
        'Опасное событие?',
        default=False,
    )
    # допустивший несоответствие
    intruder = models.ForeignKey(
        Profile,
        on_delete=SET_NULL,
        related_name='intruder',
        verbose_name='Допустивший несоответствие',
        null=True,
    )
    # не выявивший несоответствие на ниженем уровне
    unseeing = models.ForeignKey(
        Profile,
        on_delete=SET_NULL,
        related_name='unseeing',
        verbose_name='Не выявивший несоответствие',
        null=True,
    )
    section_esupb = models.CharField(
        'Раздел ЕСУПБ',
        max_length=150,
        blank=True,
        null=True,
    )
    inspector = models.ForeignKey(
       Profile,
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
    fix_action = models.TextField(
        'Мероприятие по устранению',
        default='Данные не введены',
        null=True,
        blank=True,
    )
    fixer = models.ForeignKey(
        Profile,
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
        default='Данные не введены',
        max_length=500,
        blank=True,
        null=True,
    )
    correct_action = models.TextField(
        'Корректирующее действие',
        default='Данные не введены',
        null=True,
        blank=True,
    )
    resources = models.TextField(
        'Необходимые ресурсы',
        default='Данные не введены',
        null=True,
        blank=True,
    )
    corrector = models.ForeignKey(
        Profile,
        verbose_name='Исполнитель',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    correct_deadline = models.DateField(
        'Срок корректировки',
        null=True,
        blank=True,
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
        verbose_name = 'несоответствие'
        verbose_name_plural = 'несоответствия'
        constraints = [
            models.UniqueConstraint(
                fields=['act', 'fault_number'],
                name='unique_fault_numbering'
            ),
        ]

    def __str__(self):
        complex_note = (f'{self.location} - {self.description[:30]}')
        if len(self.description) > 30:
            return complex_note + '...'
        return complex_note

    @property
    def image_before_url(self, default_path="apk/image_not_upload.png"):
        if self.image_before:
            return self.image_before
        else:
            return default_path

    @property
    def image_after_url(self, default_path="apk/image_not_upload.png"):
        if self.image_after:
            return self.image_after
        else:
            return default_path

    @property
    def deltatime_fix(self):
        return self.deltatime_calc(self.fix_deadline, self.fixed)

    @property
    def deltatime_correct(self):
        return self.deltatime_calc(self.correct_deadline, self.corrected)

    # @property
    # def abandoned_fix(self):
    #     return self.abandoned_check(self.fix_deadline)

    # @property
    # def abandoned_correct(self):
    #     return self.abandoned_check(self.correct_deadline)

    # def abandoned_check(self, date):
    #     if action:
    #         return ['Выполнено', 0]
    #     elif date != None and not action:
    #         today = dt.datetime.today()
    #         today_now = dt.datetime(today.year, today.month, today.day)
    #         deadline = dt.datetime(date.year, date.month, date.day)
    #         if today_now == deadline:
    #             return ['сегодня последний день', 1]
    #         elif today_now > deadline:
    #             deltatime = today_now - deadline
    #             return [f'/ просрочено дней: {deltatime.days} /', 2]
    #         deltatime = deadline - today_now
    #         return [f'/ осталось дней: {deltatime.days} /', 1]

    # определение количества оставшихся дней и дней просрочки
    def deltatime_calc(self, date, action):
        if action:
            return ['/ выполнено /', 0]
        elif date != None and not action:
            today = dt.datetime.today()
            today_now = dt.datetime(today.year, today.month, today.day)
            deadline = dt.datetime(date.year, date.month, date.day)
            if today_now == deadline:
                return ['/ сегодня последний день /', 1]
            elif today_now > deadline:
                deltatime = today_now - deadline
                return [f'/ просрочено дней: {deltatime.days} /', 2]
            deltatime = deadline - today_now
            return [f'/ осталось дней: {deltatime.days} /', 1]
