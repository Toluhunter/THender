from . import setup_asgi

from django.core.asgi import get_asgi_application
from django.conf import settings

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack

from transmission.router import websocket_urlpatterns
from transmission.models import Online, Transfer
from .middleware import JWTAuthMiddleWare


setup_asgi

# If Production Environment Is Starting Delete Online Table

if settings.DEBUG:
    '''
    Prevent false online users after server is restarted
    '''
    Online.objects.all().delete()
    Transfer.objects.all().delete()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket":
            SessionMiddlewareStack(
            JWTAuthMiddleWare(
                URLRouter(websocket_urlpatterns)
            )
        )
    }
)
