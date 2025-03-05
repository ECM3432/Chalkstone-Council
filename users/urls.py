# core/urls.py
from django.urls import path
from core import views

urlpatterns = [
    path('users/', views.home, name='users'),  # homepage view
]