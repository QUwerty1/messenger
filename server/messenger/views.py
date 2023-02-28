from django.shortcuts import render
from models import Message


def index():
    return render(template_name='messenger/index.html')

