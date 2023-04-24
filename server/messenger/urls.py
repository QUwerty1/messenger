from django.urls import path
from . import views


urlpatterns = [
    path('ping/', views.ping, name='ping'),
    path('iue/', views.is_user_exists, name='iue')
]
