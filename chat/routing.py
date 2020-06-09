from . import consumers

from django.conf.urls import url
from django.urls import re_path, path

websocket_urlpatterns = [
    re_path(r'^ws$', consumers.ChatConsumer),
    #path('ws/', consumers.ChatConsumer)
]
