from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('register-member/', views.register_member, name='register_member'),
    path('register-trainer/', views.register_trainer, name='register_trainer'),
    path('register-staff/', views.register_staff, name='register_staff'),
    path('community_page/', views.community_page, name='community_page'),
    path('', views.homepage, name='homepage'),
    # Add more URL patterns for other views as needed
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)