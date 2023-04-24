from channels.routing import ProtocolTypeRouter, URLRouter
from messenger.views import web_sockets
from django.urls import path
websockets = URLRouter([
    path(
        "ws/",
        web_sockets,
        name="live-score",
    ),
])