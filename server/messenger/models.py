from django.db import models
import json
from users.models import CustomUser as User

encoder = json.JSONEncoder()
decoder = json.JSONDecoder()


# class User(models.Model):
#     def __str__(self):
#         return f"{self.id}. {self.firstname} {self.email}"
#
#     id = models.AutoField().primary_key
#     email = models.EmailField()
#     firstname = models.CharField(max_length=30)
#     surname = models.CharField(max_length=30)
#     gender = models.CharField(max_length=1)
#     chats = models.JSONField()
#     info = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):

    def __str__(self):
        return f"{self.id}. {self.name}"

    @staticmethod
    def create(name: str, user: User):
        chat = Chat(name=name, users=json.loads(user.id))
        chat.save()
        return chat

    @staticmethod
    def add_user(chat_id: int, user: User):
        chat = Chat.objects.filter(id=chat_id)

        users = decoder.decode(chat.users)
        users.append(user.id)
        chat.users = encoder.encode(user)

        chats = decoder.decode(user.chats)
        chats.append(chat.id)
        user.chats = encoder.encode(chat)

        chat.save()

        return chat

    id = models.AutoField().primary_key
    name = models.CharField(max_length=30)
    users = models.JSONField()


class Content(models.Model):

    def __str__(self):
        return f"{self.id}: {self.text[0:50]}"

    @staticmethod
    def create(text: str, files: list):
        content = Content(text=text, files=files)
        content.save()
        return content

    id = models.AutoField().primary_key
    text = models.TextField()
    files = models.JSONField(default=encoder.encode([]))


class Message(models.Model):

    def __str__(self):
        return f"{self.author}: {self.content}"

    @staticmethod
    def create(user: User, text: str, files: list, chat: Chat):
        content = Content.create(text=text, files=files)
        message = Message(author=user, chat=chat, content=content)
        message.save()
        return message

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.OneToOneField(Content, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
