from django.contrib import admin

from .models import Act, Fault, User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('last_name',)
    list_filter = ('last_name',)
    empty_value_display = '-пусто-'

class ActAdmin(admin.ModelAdmin):
    list_display = ('year', 'number', 'compile_data',)
    search_fields = ('year',)
    list_filter = ('number',)
    empty_value_display = '-пусто-'

class FaultAdmin(admin.ModelAdmin):
    list_display = (
        'control_level',
        'group',
        'act',
        'location',
        'document',
        'section_esupb',
        'inspector',
        'intruder',
        'image_before',
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
    search_fields = ('location', 'group', 'inspector',)
    list_filter = ('group',)
    empty_value_display = '-пусто-'

admin.site.register(Act, ActAdmin)
admin.site.register(Fault, FaultAdmin)
admin.site.register(User, UserAdmin)