# core/urls.py
from django.urls import path
from core import views

urlpatterns = [
    path('analytics/', views.home, name='analytics'),  # homepage view
]