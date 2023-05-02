from django.http import HttpResponse
from users.models import CustomUser
import messenger.models as models
import json
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect

# Просто функции


def json_response(content, dump=True):
    if dump:
        content = json.dumps(content)
    return HttpResponse(
        status=200,
        content_type='text/json; charset=utf-8',
        content=content
    )


@require_POST
@login_required
def add_user(request):
    chat_id = request.POST.get('chat_id')
    user_id = request.POST.get('user_id')
    chat = models.Chat.objects.filter(id=chat_id).first()
    if request.user.id not in json.loads(chat.users):
        return HttpResponse(status=403, reason='access denied')
    users = json.loads(chat.users)
    users.append(user_id)
    models.Chat.objects.filter(id=chat_id).update(users=users)

# Чаты


@require_POST
@login_required
def get_chat(request):

    chat_id = request.POST.get('chat_id')
    chat = models.Chat.objects.filter(id=chat_id).first()
    if chat is None:
        return HttpResponse(status=404, reason='no chat')
    if request.user.id not in json.loads(chat.users):
        return HttpResponse(status=403, reason='access denied')

    messages = models.Message.objects.filter(chat=chat).order_by('created_at').all()
    content = []
    for message in messages:
        content.append({
            'id': message.id,
            'author_first_name': message.author.first_name,
            'author_last_name': message.author.last_name,
            'text': message.content.text,
            'files': message.content.files,
            'create_at': str(message.created_at),
            'updated_at': str(message.updated_at)
        })
    return json_response(content)


@require_POST
@login_required
def get_chats(request):
    user = CustomUser.get_user_model(request)
    chats = []
    for chat in json.loads(user.chats):

        chats.append({
            'id': chat,
            'name': models.Chat.objects.filter(id=chat).first().name
        })
    return json_response(chats, False)


@require_POST
@login_required
def create_chat(request):
    chat_name = request.POST.get('chat_name')
    if chat_name == '' or chat_name is None:
        return HttpResponse(status=400)
    chat = models.Chat.create(chat_name, request.user.id)

    user = CustomUser.get_user_model(request)
    chats = json.loads(user.chats)
    chats.append(chat.id)
    chats = json.dumps(chats)
    CustomUser.objects.filter(id=request.user.id).update(chats=chats)

    return HttpResponse(status=200)

# Сообщения


@require_POST
@login_required
def to_message(request):
    chat_id = request.POST.get('chat_id')
    text = request.POST.get('text')
    user = CustomUser.get_user_model(request)
    chat = models.Chat.objects.filter(id=chat_id).first()
    if user.id not in json.loads(chat.users):
        return HttpResponse(status=403, reason='access denied')
    models.Message.create(user, text, list(), chat)
    return HttpResponse(status=200)


@require_POST
@login_required
def change_message(request):
    message_id = request.POST.get('message_id')
    text = request.POST.get('text')
    message = models.Message.objects.filter(id=message_id).first()
    if message.author.id != request.user.id:
        return HttpResponse(status=403, reason='access denied')
    models.Content.objects.filter(message=message).update(text=text)
    return HttpResponse(status=200)


@require_POST
@login_required
def delete_message(request):
    message_id = request.POST.get('message_id')
    message = models.Message.objects.filter(id=message_id).first()
    if message.author.id != request.user.id:
        return HttpResponse(status=403, reason='access denied')
    models.Content.objects.filter(message=message).delete()
    return HttpResponse(status=200)

# Тесто


def test(request):
    return HttpResponse(request.FILES.keys())


@require_POST
def token(request):
    return HttpResponse(json.dumps({
        'token': get_token(request)
    }))


def ping(request):
    name = request.POST.get('login')
    password = request.POST.get('password')
    text = json.dumps({
        'login': name,
        'password': password
    })
    return HttpResponse(text)

