from django.urls import path
from . import views

urlpatterns = [
    path('', views.device_list, name='device_list'),
    path('toggle/<int:device_id>/', views.toggle_device, name='toggle_device'),
]
