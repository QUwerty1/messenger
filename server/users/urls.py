from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('not_auth/', views.user_not_auth, name='not_auth'),
    path('user/', views.get_user_data, name='user'),
    path('change_data/', views.change_user_data, name='change_data'),
    path('is_auth/', views.is_user_auth, name='is_auth'),
    path('register/', views.register, name='register')
]
