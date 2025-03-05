# core/urls.py
from django.urls import path
from core import views

urlpatterns = [
    path('comments/', views.home, name='comments'),  # homepage view
]