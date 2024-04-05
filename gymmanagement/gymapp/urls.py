from django.urls import path
from . import views

urlpatterns = [
    path('register-member/', views.register_member, name='register_member'),
    # Add more URL patterns for other views as needed
]