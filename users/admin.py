from django.contrib import admin

from .models import Department, Profile, User


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


admin.site.register(Department, DepartmentAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
