from django.urls import path
from .views import FetchTransmissionList

urlpatterns = [
    path("", FetchTransmissionList.as_view(), name="transmissions")
]
