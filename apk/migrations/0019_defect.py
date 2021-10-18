# Generated by Django 3.2 on 2021-10-05 16:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apk', '0018_auto_20211005_2111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Defect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('journal', models.CharField(choices=[('Буфер', 'Buffer'), ('Журнал выдачи производственных заданий', 'Journal Of Tasks'), ('Журнал дефектов основного и вспомогательного оборудования', 'Journal Of Defects'), ('Журнал АПК', 'Journal Apk'), ('Ведомость дефектов и несоответствий', 'Sheet Of Defects')], default='Буфер', max_length=100, verbose_name='Журнал')),
                ('find_date', models.DateTimeField(auto_now_add=True, verbose_name='Время обнаружения')),
                ('description', models.TextField(verbose_name='Описание дефекта')),
                ('danger', models.BooleanField(default=True, verbose_name='Опасное событие?')),
                ('fix_action', models.TextField(verbose_name='Мероприятия по устранению')),
                ('fix_deadline', models.DateTimeField(verbose_name='Планируемые сроки устранения')),
                ('fix_done', models.BooleanField(default=True, verbose_name='Устранено')),
                ('finder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='finder', to='apk.profile', verbose_name='Выявивший дефект')),
                ('fixer_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fixer_1', to='apk.profile', verbose_name='Исполнитель №1')),
                ('fixer_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fixer_2', to='apk.profile', verbose_name='Исполнитель №2')),
                ('fixer_3', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fixer_3', to='apk.profile', verbose_name='Исполнитель №3')),
                ('lead_fixer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lead_fixer', to='apk.profile', verbose_name='Ответственный за устранение')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='defect', to='apk.location', verbose_name='Место обнаружения')),
            ],
        ),
    ]
