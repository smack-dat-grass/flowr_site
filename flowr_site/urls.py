"""flowr_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.urls import include, path
from django.contrib import admin
from flowr_site import views

from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from .password_reset.views import password_reset
urlpatterns = [
    path('', views.index, name='index'),
    path('get_flowr_site_health/', views.get_flowr_site_health, name='get_flowr_site_health'),
    path('admin/', admin.site.urls),
    path('redirect/<str:path>/', views.redirect),
    path('accounts/', include('django.contrib.auth.urls')),
    path('reports/', include('reports.urls')),
    path('tasks/', include('tasks.urls')),
    path('config/', include('config.urls')),
    path('alerts/', include('alerts.urls')),
    path('search/', include('search.urls')),
    path('config/', include('config.urls')),
    path('api/', include('api.urls')),
    path('tools/', include('tools.urls')),
    path('status/', include('health_check.urls')),
    path('django-rq/', include('django_rq.urls')),
    url(r'password_reset/', password_reset, name='password_reset'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler404 = 'flowr_site.views.handler404'
handler500 = 'flowr_site.views.handler500'

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
