from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        models = User
        fields = ('username', 'email', 'password')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        models = User
        fields = ('first_name', 'last_name', 'info')