"""
ASGI config for src project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from src.infrastructure.web.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

application = ProtocolTypeRouter(
    {
        # HTTP handling by Django
        "http": get_asgi_application(),
        # WebSocket handling by Channels
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
