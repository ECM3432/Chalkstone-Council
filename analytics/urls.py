# analytics/urls.py
from django.urls import path
from analytics import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('analytics/', views.home, name='analytics'),  # homepage view
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)