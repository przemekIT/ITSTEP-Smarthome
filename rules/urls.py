from django.urls import path
from . import views

urlpatterns = [
    path('', views.rules_home, name='rules_home'),
    path('run/', views.run_rules, name='run_rules'),
]
