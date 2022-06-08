from django.urls import path

from . import views

app_name = 'apk'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>/', views.index_apk, name='index_control'),
    # следующие эндпоинты для 3 и 4 уровней АПК
    path('<slug:slug>/acts/new/', views.act_new, name='act_new'),
    path(
        '<slug:slug>/acts/<int:act_year>/<int:act_number>/',
        views.single_act,
        name='single_act'
    ),
    path(
        '<slug:slug>/acts/<int:act_year>/<int:act_number>/fault-new/',
        views.fault_new,
        name='fault_new'
    ),
    path(
        ('<slug:slug>/acts/<int:act_year>/<int:act_number>/'
         'fault-edit/<int:fault_number>/'),
        views.fault_edit,
        name='fault_edit'),
    path(
        ('<slug:slug>/acts/<int:act_year>/<int:act_number>/'
         'faults/<int:fault_number>/'),
        views.single_fault_act,
        name='single_fault_act'
    ),
    path(
        '<slug:slug>/acts/<int:act_year>/<int:act_number>/plan/',
        views.single_plan,
        name='single_plan'
    ),
    path(
        ('<slug:slug>/acts/<int:act_year>/<int:act_number>/plan/'
         'faults/<int:fault_number>/fix-new/'),
        views.fix_new,
        name='fix_new'
    ),
    path(
        ('<slug:slug>/acts/<int:act_year>/<int:act_number>/plan/'
         'faults/<int:fault_number>'),
        views.single_fault_plan,
        name='single_fault_plan'
    ),
    # сохранение акта в excel
    path(
        '<slug:slug>/acts/<int:act_year>/<int:act_number>/export/',
        views.export_act_excel,
        name='export_act_excel'
    ),
    path(
        '<slug:slug>/acts/<int:act_year>/<int:act_number>/plan/export/',
        views.export_plan_excel,
        name='export_plan_excel'
    ),
    # здесь эндпоинты для первого уровня АПК
    # для корректной работы первого уровня слаг должен быть '1_apk'
    path(
        '<slug:slug>/faults',
        views.index_first_level,
        name='index_first_level'
    ),
    path(
        '<slug:slug>/fault-new',
        views.first_level_fault_new,
        name='first_level_fault_new'
    ),
    path(
        '<slug:slug>/fault/<int:fault_number>',
        views.first_level_single_fault,
        name='first_level_single_fault'
    )
]
