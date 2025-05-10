# src/infrastructure/web/routing.py
from django.urls import re_path

from src.infrastructure.web.consumer import Consumer

# Routing to the URL Consumer which
# will handle the chat functionality.
websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<chat_id>\d+)/$", Consumer.as_asgi()),
]
