# Generated by Django 3.2 on 2021-10-01 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apk', '0009_auto_20211001_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fault',
            name='fault_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления несоответствия'),
        ),
    ]