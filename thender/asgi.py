import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from transmission.router import websocket_urlpatterns
from .middleware import JWTAuthMiddleWare

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thender.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket":
            JWTAuthMiddleWare(
                URLRouter(websocket_urlpatterns)
        )
    }
)
