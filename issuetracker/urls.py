"""
URL configuration for issuetracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('core.urls')),                # core app (home, etc.)
    path('issues/', include('issues.urls')),       # issues app
    path('comments/', include('comments.urls')),   # comments app
    path('analytics/', include('analytics.urls')), # analytics app
    path('users/', include('users.urls')),         # users app (if needed for profile)
    path('admin/', admin.site.urls),               # django admin
    path('accounts/', include('django.contrib.auth.urls')), # django auth
    path('accounts/', include('allauth.urls')),  # Allauth for social logins like Google OAuth
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)