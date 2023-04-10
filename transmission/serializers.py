from rest_framework import serializers

from account.serializers import FetchUserSerializer
from .models import Transmission, History


class TransmissionSerializer(serializers.ModelSerializer):

    sender = FetchUserSerializer(read_only=True)
    reciever = FetchUserSerializer(read_only=True)

    class Meta:
        model = Transmission
        fields = [
            "id",
            "file_name",
            "total_size",
            "bytes_sent",
            "accepted",
            "sender",
            "reciever",
            "start_date"
        ]
        read_only_fields = ["id", "bytes_sent", "accepted", "start_date"]


class CreateTransmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transmission
        fields = [
            "id",
            "reciever",
            "file_name",
            "file_location",
            "file_hash",
            "total_size"
        ]
        read_only_fields = [
            "id"
        ]

    def validate(self, attrs):
        user = self.context["request"].user

        if not user.peer.peers.filter(id=attrs["reciever"].id).exists():
            raise serializers.ValidationError("Reciever is not one of your peers")

        return attrs

    def create(self, validated_data):
        request = self.context["request"]

        return Transmission.objects.create(
            sender=request.user,
            **validated_data
        )


class HistorySerializer(serializers.ModelSerializer):

    transmission_status = serializers.SerializerMethodField()

    def get_transmission_status(self, obj):
        for value, name in History.choices:
            if value == obj.status:
                return name

    class Meta:
        model = History
        exclude = ["status"]
