# Generated by Django 3.2 on 2021-10-05 16:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apk', '0016_alter_location_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('manager', 'Manager'), ('lead', 'Lead'), ('engineer', 'Engineer'), ('employee', 'Employee')], default='employee', max_length=30, verbose_name='Роль пользователя'),
        ),
        migrations.AlterField(
            model_name='fault',
            name='act',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='faults', to='apk.act', verbose_name='Номер акта'),
        ),
        migrations.AlterField(
            model_name='fault',
            name='fault_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления несоответствия'),
        ),
    ]
