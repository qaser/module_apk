from django.contrib import admin
from .models import Quote


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'source', 'article')
    search_fields = ('text', 'source',)
    list_filter = ('source',)


admin.site.register(Quote, QuoteAdmin)
