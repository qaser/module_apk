from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_level_3, name='index'),
    path('acts/<int:act_year>/<int:act_number>/', views.single_act, name='single_act'),
    path('acts/<int:act_year>/<int:act_number>/<int:fault_id>/', views.single_fault_act, name='single_fault_act'),
    # path('acts/<int:act_id/fault/new/', views.new_fault, name='new_fault'),
    # path('acts/new/', views.act_new, name='act_new'),
    path('acts/<int:act_year>/<int:act_number>/plan/', views.single_plan, name='single_plan'),
    # path('plans/<int:plan_id>/fault/<fault_id>', views.single_fault_plan, name='single_fault_plan'),
    # path('plans/<int:plan_id/fix/new/', views.new_fix, name='new_fix'),
]
