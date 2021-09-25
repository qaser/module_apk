from django.contrib import admin

from .models import Act, Fault, Location, Fix, Department, Profile, User, Control
from django.contrib import admin


class ControlAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title',)
    list_filter = ('title',)
    empty_value_display = '-пусто-'


class ProfileInline(admin.StackedInline):
    model = Profile
    

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_name', 'first_name',)
    empty_value_display = '-пусто-'
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
    list_display = ('control_level', 'act_number', 'act_year', 'act_compile_date',)
    search_fields = ('act_year',)
    list_filter = ('control_level', 'act_number',)
    empty_value_display = '-пусто-'


class FaultAdmin(admin.ModelAdmin):
    list_display = (
        'act',
        'location',
        'description',
        'inspector',
        'image_before',
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
admin.site.register(User, UserAdmin)