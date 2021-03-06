# Generated by Django 3.2 on 2021-10-05 18:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apk', '0019_defect'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='defect',
            name='fixer_1',
        ),
        migrations.RemoveField(
            model_name='defect',
            name='fixer_2',
        ),
        migrations.RemoveField(
            model_name='defect',
            name='fixer_3',
        ),
        migrations.AddField(
            model_name='defect',
            name='control_level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='control_defect', to='apk.control', verbose_name='Уровень АПК'),
        ),
        migrations.AlterField(
            model_name='defect',
            name='find_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время обнаружения'),
        ),
    ]
