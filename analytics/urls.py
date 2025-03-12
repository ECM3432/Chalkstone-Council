# analytics/urls.py
from django.urls import path
from analytics import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.analytics_home, name='analytics_home'),  # Home page
    path('issues/', views.analytics_stats, name='analytics_stats'),  # Page 1: Overview of Issues by Status
    path('filter/', views.analytics_filter, name='analytics_filter'),  # Page 2: Filter and Query Issues
    path('closed-issues/', views.analytics_issues, name='analytics_issues'),  # Page 3: View Closed Issues
    path('charts/', views.analytics_charts, name='analytics_charts'),  # Page 4: Visualize Issues in Charts
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)