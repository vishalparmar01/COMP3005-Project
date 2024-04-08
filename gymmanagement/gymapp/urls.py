from django.urls import path
from . import views

urlpatterns = [
    path('register-member/', views.register_member, name='register_member'),
    path('register-trainer/', views.register_trainer, name='register_trainer'),
    path('register-staff/', views.register_staff, name='register_staff'),
    path('', views.homepage, name='homepage'),
    # Add more URL patterns for other views as needed
]