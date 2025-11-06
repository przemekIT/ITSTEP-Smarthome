from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'room', 'type', 'status', 'value', 'last_updated')
    list_filter = ('type', 'status')
    search_fields = ('name', 'room')
