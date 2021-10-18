# Generated by Django 3.2 on 2021-10-01 07:02

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apk', '0008_alter_fault_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='act',
            options={'ordering': ('-act_year',), 'verbose_name': 'акт', 'verbose_name_plural': 'акты'},
        ),
        migrations.AddField(
            model_name='fault',
            name='fault_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 1, 12, 2, 20, 72885), verbose_name='Дата добавления несоответствия'),
        ),
    ]