from django.db import models
from django.contrib.auth.models import AbstractUser
import json


class User(AbstractUser):
    id = models.AutoField().primary_key
    gender = models.CharField(max_length=1)
    chats = models.JSONField(default=json.JSONEncoder.encode([]))
    info = models.TextField(default="")

    def __str__(self):
        return f"{self.id}: {super().username}"
