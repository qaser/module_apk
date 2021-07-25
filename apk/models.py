from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import TextField
from django.db.models.fields.related import ForeignKey


User = get_user_model()


class Protocol(models.Model):
    number = models.PositiveSmallIntegerField('номер протокола',)
    compile_data = models.DateField('дата составления', auto_now_add=True)


class Fault(models.Model):
    description = models.TextField('описание несоответствия', max_length=500,)
    document = models.TextField('нормативный документ', max_length='150',)
    