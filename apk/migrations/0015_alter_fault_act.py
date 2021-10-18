# Generated by Django 3.2 on 2021-10-03 00:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apk', '0014_alter_fix_fault'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fault',
            name='act',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faults', to='apk.act', verbose_name='Номер акта'),
        ),
    ]
