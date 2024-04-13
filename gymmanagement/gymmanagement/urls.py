"""
URL configuration for gymmanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.views.generic import RedirectView
from gymapp import views  # Import your views from gymapp
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register-member/', views.register_member, name='register_member'),
    path('register-trainer/', views.register_trainer, name='register_trainer'),
    path('register-staff/', views.register_staff, name='register_staff'),
    path('community_page/', views.community_page, name='community_page'),
    path('homepage/', views.homepage),
    path('', views.homepage),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
