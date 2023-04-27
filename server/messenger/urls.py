from django.urls import path
from . import views


urlpatterns = [
    path('ping/', views.ping, name='ping'),
    path('login/', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('token/', views.token, name='token'),
    path('test/', views.test, name='test'),
    path('user/', views.get_user_data, name='user'),
    path('change_data/', views.change_user_data, name='change_data')
]
