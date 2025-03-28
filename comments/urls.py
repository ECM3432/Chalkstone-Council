# comments/urls.py
from django.urls import path
from comments import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('add/<int:issue_id>/', views.add_comment, name='add_comment')  # add comment view
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)