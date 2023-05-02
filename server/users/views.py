from django.shortcuts import render
from messenger.views import json_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from users.models import CustomUser
from users.forms import CustomUserCreationForm


@require_POST
def is_user_auth(request):
    return json_response(request.user.is_authenticated)


def user_not_auth(request):
    return HttpResponse(
        status=401,
        reason='not auth'
    )


@require_POST
def register(request):
    res = 1
    data = {
        'email': request.POST.get('email'),
        'first_name': request.POST.get('first_name'),
        'last_name': request.POST.get('last_name'),
        'username': request.POST.get('username'),
        'password': request.POST.get('password')
    }
    for var in data:
        if (data[var] == '') or (data[var] is None):
            res = 0
    # user = CustomUser(data['email'], data['email'], data['email'], data['email'], data['email'])
    form = CustomUserCreationForm(request.POST)
    if not form.is_valid():
        res = 0
    if res == 0:
        return HttpResponse(form.errors, status=406, reason='invalid data')
    user = form.save()
    login(request, user)
    return HttpResponse(status=200)


@require_POST
def log_in(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
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


@require_POST
def log_out(request):
    logout(request)
    return HttpResponse(status=200)


@require_POST
@login_required
def get_user_data(request):
    user_id = request.POST.get('user_id')
    if user_id is None:
        user_id = request.user.id
    user = CustomUser.objects.filter(id=user_id).first()
    if user is None:
        return HttpResponse(status=406, reason='invalid data')

    return json_response({
        'icon': user.icon,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'gender': user.gender,
        'info': user.info,
    })


@require_POST
@login_required
def change_user_data(request):

    attrs = {
        'firs_name': request.POST.get('first_name'),
        'last_name': request.POST.get('last_name'),
        'gender': request.POST.get('gender'),
        'info': request.POST.get('info')
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
