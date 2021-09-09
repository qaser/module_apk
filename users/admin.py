from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'patronymic',
        'job_position',
    )
    search_fields = ('last_name', 'job_position',)
    list_filter = ('job_position',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
