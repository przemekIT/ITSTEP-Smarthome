from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('accounts/', views.accounts, name='accounts'),
    path('accounts/details/<int:id>', views.details, name='details'),
    path('testing/', views.testing, name='testing'),    
]