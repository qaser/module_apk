from django.contrib import admin

from .models import Message, Quote


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'source', 'article')
    search_fields = ('text', 'source',)
    list_filter = ('source',)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'date_created',)
    search_fields = ('author', 'date_created',)
    list_filter = ('author', 'date_created',)


admin.site.register(Quote, QuoteAdmin)
admin.site.register(Message, MessageAdmin)
