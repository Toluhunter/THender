from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.serializers import FetchUserSerializer
from . import serializers
from .models import PeerRequest


class CreatePeerRequestView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.RequestSerializer


class FetchPeerRequestView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.FetchRequestSerializer

    def get_queryset(self):
        type_requests = self.request.GET.get("type", None)

        if not type_requests:
            return PeerRequest.objects.filter(sender=self.request.user)

        if type_requests == "recieved":
            return PeerRequest.objects.filter(user=self.request.user)

        return PeerRequest.objects.filter(sender=self.request.user)


class ReplyPeerRequestView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ReplyPeerRequestSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response({"message": "Action Performed Successfully"})


class PeerView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = FetchUserSerializer

    def get_queryset(self):
        user = self.request.user

        return user.peer.peers.all()
