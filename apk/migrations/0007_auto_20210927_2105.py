# Generated by Django 3.2 on 2021-09-27 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apk', '0006_alter_fault_image_before'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='title',
            field=models.CharField(max_length=50, unique=True, verbose_name='название службы'),
        ),
        migrations.AlterField(
            model_name='location',
            name='object',
            field=models.CharField(max_length=100, unique=True, verbose_name='оборудование'),
        ),
    ]
