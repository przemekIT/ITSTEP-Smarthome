from django.contrib import admin
from .models import Rule

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled', 'sensor', 'comparator', 'threshold', 'target', 'action', 'last_triggered')
    list_filter = ('enabled', 'comparator', 'action')
    search_fields = ('name', 'sensor__name', 'target__name')
