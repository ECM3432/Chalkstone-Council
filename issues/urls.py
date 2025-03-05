# issues/urls.py

from django.urls import path
from core import views

urlpatterns = [
    path('issues/', views.home, name='issues'),  # homepage view
]