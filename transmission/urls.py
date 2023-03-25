from django.urls import path
from .views import (
    FetchTransmissionListView,
    AddTransmissionView,
    DeleteTransmissionView,
    AcceptTransmisionRequest,
    PendingTransmissionView,
    TransmissionHistoryView
)

urlpatterns = [
    path("all/", FetchTransmissionListView.as_view(), name="transmissions"),
    path("add/", AddTransmissionView.as_view(), name="add-transmission"),
    path("pending/", PendingTransmissionView.as_view(), name="pending"),
    path("history/", TransmissionHistoryView.as_view(), name="history"),
    path("accept/<uuid:id>/", AcceptTransmisionRequest.as_view(), name="accept-transmission"),
    path("delete/<uuid:id>/", DeleteTransmissionView.as_view(), name="delete")
]
