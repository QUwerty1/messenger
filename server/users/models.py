from django.db import models
from django.contrib.auth.models import AbstractUser
import json

encoder = json.JSONEncoder()


class CustomUser(AbstractUser):
    id = models.AutoField().primary_key
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1)
    chats = models.JSONField(default=encoder.encode([]))
    info = models.TextField(default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.id}: {super().username}"
