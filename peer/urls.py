from django.urls import path

from . import views

urlpatterns = [
    path('request/', views.CreatePeerRequestView.as_view(), name="create-request"),
    path('requests/', views.FetchPeerRequestView.as_view(), name="fetch-requests"),
    path('handle-requests/', views.ReplyPeerRequestView.as_view(), name="handle-requests"),
    path('all/', views.PeerView.as_view(), name="peers")
]
