# Generated by Django 3.2 on 2021-09-25 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apk', '0003_auto_20210924_2014'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='control',
            options={'ordering': ('title',), 'verbose_name': 'тип проверки', 'verbose_name_plural': 'типы проверок'},
        ),
    ]
