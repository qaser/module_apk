from django.contrib import admin

from .models import Act, Fault, Fix, Location


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


# class PlanAdmin(admin.ModelAdmin):
#     list_display = ()
#     search_fields = ('act_year',)
#     list_filter = ('control_level', 'act_number',)
#     empty_value_display = '-пусто-'

class FaultAdmin(admin.ModelAdmin):
    list_display = (
        'act',
        'location',
        'description',
        'inspector',
    )
    search_fields = ('location', 'group', 'inspector',)
    list_filter = ('location', 'group', 'inspector',)
    empty_value_display = '-пусто-'


class FixAdmin(admin.ModelAdmin):
    list_display = (
        'fix_action',
        'fixer',
        'fix_deadline',
        'fixed',
        'fix_date',
        'image_after',
        'reason',
        'correct_action',
        'resources',
        'corrector',
        'correct_deadline',
        'corrected',
        'correct_date',
    )
    search_fields = ()
    list_filter = ()
    empty_value_display = '-пусто-'


admin.site.register(Act, ActAdmin)
admin.site.register(Fault, FaultAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Fix, FixAdmin)
