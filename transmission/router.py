from django.urls import re_path
from .consumers import TransmissionConfigConsumer, TransferDataConsumer

websocket_urlpatterns = [
    re_path(r'(?P<id>[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12})/',
            TransferDataConsumer.as_asgi()),
    re_path('', TransmissionConfigConsumer.as_asgi()),
]
