from django.db import models


class User(models.Model):

    def __str__(self):
        return f"{self.id}. {self.firstname} {self.email}"

    id = models.AutoField().primary_key
    email = models.EmailField()
    firstname = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    gender = models.CharField(max_length=1)
    chats = models.JSONField()
    info = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):

    def __str__(self):
        return f"{self.id}. {self.name}"

    id = models.AutoField().primary_key
    name = models.CharField(max_length=30)
    users = models.JSONField()


class Content(models.Model):

    def __str__(self):
        return f"{self.id}: {self.text[0:50]}"

    id = models.AutoField().primary_key
    text = models.TextField()
    files = models.JSONField()


class Message(models.Model):

    def __str__(self):
        return f"{self.author}: {self.content}"

    def add_message(self, user: User, text: str, files: list, chat: Chat):
        content = Content.object.create(text=text, files=files)
        self.object.create(author=user, chat=chat, content=content)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.OneToOneField(Content, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
