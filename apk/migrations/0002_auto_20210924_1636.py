# Generated by Django 3.2 on 2021-09-24 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apk', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='control',
            name='description',
        ),
        migrations.AlterField(
            model_name='control',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Название проверки'),
        ),
    ]
