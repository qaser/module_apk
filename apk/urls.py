from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_level_3, name='index'),
    path('acts/new/', views.act_new, name='act_new'),
    path('acts/<int:act_year>/<int:act_number>/', views.single_act, name='single_act'),
    path('acts/<int:act_year>/<int:act_number>/fault-new/', views.fault_new, name='fault_new'),
    path('acts/<int:act_year>/<int:act_number>/fault-edit/<int:fault_number>/', views.fault_edit, name='fault_edit'),
    path('acts/<int:act_year>/<int:act_number>/faults/<int:fault_number>/', views.single_fault_act, name='single_fault_act'),
    path('acts/<int:act_year>/<int:act_number>/plan/', views.single_plan, name='single_plan'),
    # path('acts/<int:act_year>/<int:act_number>/plan/faults/<int:fault_number>/fix-new/', views.fix_new, name='fix_new'),
    path('acts/<int:act_year>/<int:act_number>/plan/faults/<int:fault_number>', views.single_fault_plan, name='single_fault_plan'),
]
