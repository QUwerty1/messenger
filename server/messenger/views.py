from django.http import HttpResponse
import json
import bcrypt
from django.shortcuts import render
from users.models import CustomUser


def ping(request):
    login = request.GET.get('login')
    password = request.GET.get('password')
    text = json.dumps({
        'login': login,
        'password': password
    })
    return HttpResponse(text)


def is_user_exists(request):
    login = request.GET.get('login')
    password = request.GET.get('password')
    user = CustomUser.objects.filter(email=login).first()
    print(f'Надо {bcrypt.hashpw(password.encode(), )}')
    print(user.password[14:])
    if user is None:
        return HttpResponse('NO USER')
    else:
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')[14:]):
            return HttpResponse('INVALID PASSWORD')
        else:
            return HttpResponse(user)
