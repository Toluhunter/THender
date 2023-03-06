from django.urls import re_path
from .consumers import TransferConsumer

websocket_urlpatterns = [
    re_path(r'(?P<group>\w+)', TransferConsumer.as_asgi()),
]
