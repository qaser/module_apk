from django.db import models
from django.db.models.deletion import CASCADE
from apk.models import Profile

class Quote(models.Model):
    text = models.TextField(
        'Текст цитаты',
        null=False,
        blank=False,
    )
    source = models.CharField(
        'Источник цитаты',
        max_length=100,
        null=False,
        blank=False,
    )
    article = models.CharField(
        'Глава источника',
        max_length=20,
        null=True,
    )

    class Meta:
        verbose_name = 'Цитата'
        verbose_name_plural = 'Цитаты'

    def __str__(self):
        return '{}{}'.format(self.text[:15], '...')


class Message(models.Model):
    author = models.ForeignKey(
        Profile,
        on_delete=CASCADE,
        verbose_name='Автор',
        related_name='message',
    )
    text = models.TextField('Текст сообщения')
    date_created = models.DateField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-date_created']

    def __str__(self):
        # return '{}{}'.format(self.text[:15], '...')
        return self.text
