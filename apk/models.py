import datetime as dt

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from .utils import compress_image

User = get_user_model()


class Role(models.TextChoices):
    ADMIN = 'admin'  # всемогущий
    MANAGER = 'manager'  # член ПДК
    LEAD = 'lead'  # начальник цеха
    ENGINEER = 'engineer'  # инженер (сменный), мастер
    EMPLOYEE = 'employee'  # работник


# служба филиала
class Department(models.Model):
    title = models.CharField('название службы', max_length=50, unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'служба филиала'
        verbose_name_plural = 'службы филиала'

    def __str__(self) -> str:
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    patronymic = models.CharField(
        'Отчество',
        max_length=50,
        blank=True,
        null=True,
    )
    job_position = models.TextField('Должность', blank=True, null=True)
    department = models.ForeignKey(
        Department,
        verbose_name='Место работы',
        on_delete=SET_NULL,
        related_name='user_department',
        null=True,
    )
    role = models.CharField(
        'Роль пользователя',
        max_length=30,
        choices=Role.choices,
        default=Role.EMPLOYEE
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователей'

    # представление пользователя в виде Фамилия И.О.
    # с учетом отсутствия Отчества
    @property
    def lastname_and_initials(self):
        lastname = self.user.last_name
        initial_name = self.user.first_name[0]
        if self.patronymic is not None:
            initial_patronymic = self.patronymic[0]
            lastname_and_initials = (f'{lastname} '
                                     f'{initial_name}.{initial_patronymic}.')
        else:
            lastname_and_initials = f'{lastname} {initial_name}.'
        return lastname_and_initials

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self) -> str:
        return self.user.get_full_name()


# место обнаружения несоответствияs
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
        unique=True,
    )

    class Meta:
        ordering = ('department',)
        verbose_name = 'объект проверки'
        verbose_name_plural = 'объекты проверки'

    def __str__(self) -> str:
        return f'{self.department} | {self.object}'


class Control(models.Model):
    title = models.CharField('Название проверки', max_length=50,)
    # для работы первого и второго уровней необходимо в поле slug
    # для этих уровней указать "1_apk" и "2_apk" соответственно
    # т.к. на этих слагах завязана логика отображения начальной страницы.
    slug = models.SlugField('Путь', unique=True, max_length=50)

    class Meta:
        ordering = ('title',)
        verbose_name = 'тип проверки'
        verbose_name_plural = 'типы проверок'

    def __str__(self):
        return self.title


class Act(models.Model):
    control_level = models.ForeignKey(
        Control,
        verbose_name='Уровень проверки',
        on_delete=CASCADE,
        related_name='control'
    )
    act_year = models.IntegerField('Год регистрации акта')
    act_number = models.PositiveSmallIntegerField('Номер акта',)
    act_compile_date = models.DateField('Дата составления', auto_now_add=True)
    closed = models.BooleanField('Отработан', default=False)

    class Meta:
        ordering = ('-act_year',)
        verbose_name = 'акт'
        verbose_name_plural = 'акты'
        constraints = [
            models.UniqueConstraint(
                fields=['act_year', 'act_number', 'control_level'],
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
    fault_date = models.DateTimeField(
        'Дата добавления несоответствия',
        auto_now_add=True,
    )
    group = models.TextField(
        'Группа несоответствий',
        choices=GROUP,
    )
    act = models.ForeignKey(
        Act,
        on_delete=CASCADE,
        verbose_name='Номер акта',
        related_name='faults',
        db_index=True,
    )
    location = models.ForeignKey(
        Location,
        on_delete=CASCADE,
        verbose_name='Место обнаружения',
        related_name='location',
        db_index=True,
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
        null=True,
    )
    inspector = models.ForeignKey(
        Profile,
        on_delete=SET_NULL,
        related_name='inspector',
        verbose_name='Проверяющий',
        null=True,
    )
    image_before = models.ImageField(
        'Фото несоответствия',
        upload_to='apk/photo_before/',
        default='apk/image_not_upload.png',
        blank=True,
        null=True,
    )

    @property
    def danger_readable(self):
        if self.danger:
            return 'может'
        return 'не может'

    class Meta:
        ordering = ['fault_number']
        verbose_name = 'несоответствие'
        verbose_name_plural = 'несоответствия'
        constraints = [
            models.UniqueConstraint(
                fields=['act', 'fault_number'],
                name='unique_fault_numbering'
            ),
        ]

    def __str__(self):
        return (f'№{self.fault_number}, '
                f'Акт №{self.act.act_number}, {self.location}')

    def save(self, *args, **kwargs):  # сжатие фото перед сохранением
        super(Fault, self).save(*args, **kwargs)
        if self.image_before:
            compress_image(self.image_before)


class Fix(models.Model):
    fault = models.OneToOneField(
        Fault,
        verbose_name='Несоответствие',
        on_delete=CASCADE,
        related_name='fix',
    )
    fix_action = models.TextField(
        'Мероприятие по устранению',
        default='Данные не введены',
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
        default='apk/image_not_upload.png',
        blank=True,
        null=True,
    )
    # корректирующие действия
    reason = models.TextField(
        'Причина появления несоответствия',
        default='Данные не введены',
        max_length=500,
    )
    correct_action = models.TextField(
        'Корректирующее действие',
        default='Данные не введены',
    )
    resources = models.TextField(
        'Необходимые ресурсы',
        default='Данные не введены',
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
        verbose_name = 'мероприятие'
        verbose_name_plural = 'мероприятия'

    def __str__(self):
        return (f'Несоответствие №{self.fault.fault_number}, '
                f'{self.fault.location}')

    # связка двух моделей, если Fault создан, то и Fix создается
    @receiver(post_save, sender=Fault)
    def create_fault_fix(sender, instance, created, **kwargs):
        if created:
            Fix.objects.create(fault=instance)

    @receiver(post_save, sender=Fault)
    def save_fault_fix(sender, instance, **kwargs):
        instance.fix.save()

    @property
    def deltatime_fix(self):
        return self.deltatime_calc(self.fix_deadline, self.fixed)

    @property
    def deltatime_correct(self):
        return self.deltatime_calc(self.correct_deadline, self.corrected)

    # определение количества оставшихся дней и дней просрочки
    # в ретурне второй элемент в списке нужен для передачи состояния
    def deltatime_calc(self, date, action):
        if action:
            return ['', 0]
        elif date is not None and not action:
            today = dt.datetime.today()
            today_now = dt.datetime(today.year, today.month, today.day)
            deadline = dt.datetime(date.year, date.month, date.day)
            if today_now == deadline:
                return ['', 1]
            # сколько дней после дедлайна
            elif today_now > deadline:
                deltatime = today_now - deadline
                return [f' /{deltatime.days} дн./', 2]
            deltatime = deadline - today_now
            # сколько дней до дедлайна
            return [f' /{deltatime.days} дн./', 1]

    # сжатие и сохранене загружаемых фотографий
    def save(self, *args, **kwargs):
        super(Fix, self).save(*args, **kwargs)
        if self.image_after:
            compress_image(self.image_after)


# class Journal(models.TextChoices):
#     BUFFER = 'Буфер'
#     JOURNAL_OF_TASKS = 'Журнал выдачи производственных заданий'
#     JOURNAL_OF_DEFECTS = 'Журнал дефектов основного'
#     JOURNAL_APK = 'Журнал АПК'
#     SHEET_OF_DEFECTS = 'Ведомость дефектов и несоответствий'


# class Defect(models.Model):
#     journal = models.CharField(
#         'Журнал',
#         choices=Journal.choices,
#         default=Journal.BUFFER,
#         max_length=100,
#     )
#     control_level = models.ForeignKey(
#         Control,
#         verbose_name='Уровень АПК',
#         related_name='control_defect',
#         on_delete=SET_NULL,
#         null=True,
#     )
#     find_date = models.DateTimeField(
#         'Время обнаружения',
#         auto_now_add=True,
#         db_index=True,
#     )
#     location = models.ForeignKey(
#         Location,
#         verbose_name='Место обнаружения',
#         related_name='defect',
#         on_delete=CASCADE,
#         db_index=True
#     )
#     description = models.TextField('Описание дефекта')
#     danger = models.BooleanField('Опасное событие?', default=False)
#     finder = models.ForeignKey(
#         Profile,
#         verbose_name='Выявивший дефект',
#         related_name='finder',
#         on_delete=SET_NULL,
#         null=True,
#     )
#     fix_action = models.TextField(
#         'Мероприятия по устранению',
#         default='Данные не введены'
#     )
#     fix_deadline = models.DateTimeField(
#         'Планируемые сроки устранения',
#         default=dt.datetime.now()
#     )
#     lead_fixer = models.ForeignKey(
#         Profile,
#         verbose_name='Ответственный за устранение',
#         related_name='lead_fixer',
#         on_delete=SET_NULL,
#         null=True,
#     )
#     fix_done = models.BooleanField('Устранено', default=False)
