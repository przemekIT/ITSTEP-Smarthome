from django.urls import path
from . import views

urlpatterns = [
    path('', views.device_list, name='device_list'), # lista wszystkich urzadzen
    path('toggle/<int:device_id>/', views.toggle_device, name='toggle_device'), # zmiana stanu konkretnego urzadzenia (ON/OFF)
    path('logs/', views.event_log_list, name='event_log_list'), # lista logow zdarzen
    path('logs/export/', views.export_event_logs_csv, name='export_event_logs_csv'),  # eksport CSV
    path('add/', views.device_create, name='device_create'), # dodawanie nowego urzadzenia
    path('<int:device_id>/edit/', views.device_update, name='device_update'), # edycja urzadzenia
    path('<int:device_id>/delete/', views.device_delete, name='device_delete'), # usuwanie urzadzenia
]