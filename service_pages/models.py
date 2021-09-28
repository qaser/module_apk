from django.db import models

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
