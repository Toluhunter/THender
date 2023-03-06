from . import setup_asgi

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

from transmission.router import websocket_urlpatterns
from .middleware import JWTAuthMiddleWare

setup_asgi
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket":
            JWTAuthMiddleWare(
                URLRouter(websocket_urlpatterns)
        )
    }
)
