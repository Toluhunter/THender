from django.contrib.auth import get_user_model

from rest_framework import serializers
from .models import PeerRequest

from account.serializers import FetchUserSerializer

User = get_user_model()


class FetchRequestSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    sender = FetchUserSerializer(read_only=True)
    user = FetchUserSerializer(read_only=True)

    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        request = self.context["request"]

        type_requests = request.GET.get("type", None)

        if not type_requests:
            self.fields.pop("sender")

        if type_requests == "recieved":
            self.fields.pop("user")
            return

        self.fields.pop("sender")


class RequestSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = PeerRequest
        fields = [
            "id",
            "user",
        ]

    def validate(self, attrs):
        sender = self.context["request"].user

        if PeerRequest.objects.filter(user=attrs["user"], sender=sender).exists():
            raise serializers.ValidationError("Pending request already made to this user")

        if sender.peer.peers.filter(id=attrs["user"].id).exists():
            # If the target user for the peer request is already in users peers prevent request
            raise serializers.ValidationError("You and this users are already peers")

        if attrs["user"] == sender:
            # Prevent authenticated user from send a peer request to themselves
            raise serializers.ValidationError("You cannot send a request to yourself")

        return attrs

    def create(self, validated_data):
        sender = self.context["request"].user
        return PeerRequest.objects.create(user=validated_data["user"], sender=sender)


class ReplyPeerRequestSerializer(serializers.Serializer):

    peer_request = serializers.UUIDField(write_only=True)
    action = serializers.BooleanField(write_only=True)

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user

        peer_request = PeerRequest.objects.filter(id=attrs["peer_request"])
        if not peer_request.exists() or peer_request.first().user != user:
            raise serializers.ValidationError("Invalid request")

        peer_request = peer_request.first()
        sender = peer_request.sender

        if not attrs["action"]:
            peer_request.delete()
            return attrs

        user.peer.peers.add(sender)
        sender.peer.peers.add(user)

        peer_request.delete()
        return attrs
