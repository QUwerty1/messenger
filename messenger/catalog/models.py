import json

from django.db import models


class User(models.Model):
    id = models.AutoField().primary_key
    email = models.EmailField()
    firstname = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    gender = models.CharField(max_length=1)
    chats = models.JSONField()
    info = models.TextField().default()
    created_at = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    id = models.AutoField().primary_key
    name = models.CharField(max_length=30)
    users = models.JSONField()


class Content(models.Model):
    id = models.AutoField().primary_key
    text = models.TextField()
    files = models.JSONField().default(json.JSONEncoder().encode([]))


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
