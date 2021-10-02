from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (Act, Control, Department, Fault, Fix, Location, Profile,
                     User)


class ControlAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


class ProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1
    can_delete = False


class AccountsUserAdmin(UserAdmin):
    inlines = [ProfileInline]


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


class FixInline(admin.StackedInline):
    model = Fix


class LocationAdmin(admin.ModelAdmin):
    list_display = ('department', 'object',)
    search_fields = ('department', 'object',)
    list_filter = ('department', 'object',)
    empty_value_display = '-пусто-'


class ActAdmin(admin.ModelAdmin):
    list_display = (
        'control_level',
        'act_number',
        'act_year',
        'act_compile_date',
    )
    search_fields = ('act_year',)
    list_filter = ('control_level', 'act_number',)
    empty_value_display = '-пусто-'


class FaultAdmin(admin.ModelAdmin):
    list_display = (
        'act',
        'fault_number',
        'location',
        'description',
        'inspector',
        'fault_date',
    )
    search_fields = ('location', 'group', 'inspector',)
    list_filter = ('location', 'group', 'inspector',)
    empty_value_display = '-пусто-'
    inlines = [FixInline]


admin.site.register(Control, ControlAdmin)
admin.site.register(Act, ActAdmin)
admin.site.register(Fault, FaultAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.unregister(User)
admin.site.register(User, AccountsUserAdmin)
