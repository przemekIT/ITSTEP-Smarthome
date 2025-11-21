from django.contrib import admin
from .models import Device, SensorData, EventLog

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """
    Konfiguracja widoku listy urzadzen w panelu administracyjnym Django.
    """
    list_display = ('name', 'room', 'type', 'status', 'value', 'last_updated')
    list_filter = ('type', 'status')
    search_fields = ('name', 'room')

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    """
    Widok danych historycznych z czujników w panelu admina.
    Umozliwia szybki podglad odczytow oraz filtrowanie po urzadzeniu.
    """
    list_display = ('device', 'value', 'timestamp')
    list_filter = ('device',)
    search_fields = ('device__name',)
# Czujnik temperatury w salonie → 17,5 → 2025-11-06 10:00



@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    """
    Widok logow zdarzen w panelu admina.
    """
    list_display = ('device', 'action', 'description', 'created_at')
    list_filter = ('action', 'device')
    search_fields = ('description', 'device__name')