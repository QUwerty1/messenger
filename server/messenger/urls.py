from django.urls import path
from . import views


urlpatterns = [
    path('ping/', views.ping, name='ping'),
    path('token/', views.token, name='token'),
    path('test/', views.test, name='test'),
    path('add_user', views.add_user, name='add_user'),
    path('chat/', views.get_chat, name='get_chat'),
    path('chats/', views.get_chats, name='get_chats'),
    path('create_chat/', views.create_chat, name='create_chat'),
    path('message/', views.to_message, name='message'),
    path('change_message/', views.change_message, name='change_message'),
    path('delete_message/', views.delete_message, name='delete_message'),
    # path('', views, name=''),

]
