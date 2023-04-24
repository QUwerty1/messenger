from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        models = CustomUser
        fields = ('username', 'email', 'password')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        models = CustomUser
        fields = ('first_name', 'last_name', 'gender', 'info')
