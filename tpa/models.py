from django.db import models

class Valve(models.Model):
    branch = models.TextField(
        verbose_name='Филиал',
    )
    department = models.TextField(
        'Наименование службы',
    )
    location = models.TextField(
        'Место установки',
    )
    title = models.TextField(
        'Наименование ТПА',
    )
    diameter = models.TextField(
        'Условный диаметр',
    )
    pressure = models.TextField(
        'Условное давление',
    )
    type_valve = models.TextField(
        'Тип ТПА',
    )
    factory = models.TextField(
        'Изготовитель',
    )
    year_made = models.TextField(
        'Год изготовления',
    )
    year_exploit = models.TextField(
        'Год ввода в эксплуатацию',
    )
    type_drive = models.TextField(
        'Тип привода',
    )
    drive_factory = models.TextField(
        'Изготовитель привода',
    )
    drive_year_exploit = models.TextField(
        'Год ввода в эксплуатацию привода',
    )
    tech_number =  models.TextField(
        'Технологический номер',
    )
    factory_number = models.TextField(
        'Заводской номер',
    )
    inventory_number = models.TextField(
        'Инвентарный номер',
    )
    register_number = models.TextField(
        'Регистрационный номер',
    )
    document = models.TextField(
        'Наличие паспорта',
    )
    lifetime = models.TextField(
        'Срок службы',
    )
    remote = models.TextField(
        'Дистанционное управление',
    )
    label = models.TextField(
        'Марка',
    )
    design = models.TextField(
        'Исполнение',
    )
    description = models.TextField(
        'Примечание',
    )
