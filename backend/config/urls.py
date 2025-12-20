"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from . import admin as admin_config  # Импортируем для настройки админки

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/lodges/', include('lodges.urls')),
    path('api/activities/', include('activities.urls')),
    path('api/events/', include('events.urls')),
    path('api/news/', include('news.urls')),
    path('api/restaurant/', include('restaurant.urls')),
    path('api/', include('core.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # В режиме разработки STATIC_URL обслуживается автоматически через runserver из папок приложений.
    # Ручное добавление static(settings.STATIC_URL...) может конфликтовать, если STATIC_ROOT существует.
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
