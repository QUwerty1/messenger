from django.http import HttpResponse
from users.models import CustomUser
import json
from django.contrib.auth import login, authenticate, logout
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


def ping(request):
    name = request.GET.get('login')
    password = request.GET.get('password')
    text = json.dumps({
        'login': name,
        'password': password
    })
    return HttpResponse(text)


@csrf_exempt
def log_in(request):

    email = request.GET.get('email')
    password = request.GET.get('password')
    user = authenticate(username=email, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse(
            status=200
        )
    else:
        return HttpResponse(
            status=406,
            reason='invalid password or email'
        )


def log_out(request):
    logout(request)
    return HttpResponse(status=200)


def get_user_data(request):
    if not request.user.is_authenticated:
        return HttpResponse(
            status=403,
            reason='not auth'
        )
    user = CustomUser.get_user_model(request)

    return HttpResponse(
        status=200,
        content=json.dumps({
            'icon': user.icon,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender': user.gender,
            'info': user.info,
        })
    )


def change_user_data(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=403, reason='not auth')
    attrs = {
    'firs_name': request.GET.get('first_name'),
    'last_name': request.GET.get('last_name'),
    'gender': request.GET.get('gender'),
    'info': request.GET.get('info')
    }

    for key in attrs.keys():
        if attrs[key] is None:
            attrs[key] = ' '

    user_id = request.user.id
    CustomUser.objects.filter(id=user_id).update(
        first_name=attrs['firs_name'],
        last_name=attrs['last_name'],
        gender=attrs['gender'],
        info=attrs['info']
    )
    return HttpResponse(status=200)


def token(request):
    return HttpResponse(json.dumps({
        'token': get_token(request)
    }))


@csrf_exempt
def test(request):
    context = request.POST.get('var')
    print(context)
    return render(request, 'index.html')
