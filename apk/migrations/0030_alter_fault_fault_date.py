# Generated by Django 3.2 on 2021-10-18 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apk', '0029_alter_fault_fault_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fault',
            name='fault_date',
            field=models.DateField(verbose_name='Дата добавления несоответствия'),
        ),
    ]
