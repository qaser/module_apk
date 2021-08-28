from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role'
    )
    search_fields = ('last_name', 'username',)
    list_filter = ('role',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
