from rest_framework import serializers

from account.serializers import FetchUserSerializer
from .models import Transmission


class TransmissionSerializer(serializers.ModelSerializer):

    sender = FetchUserSerializer(read_only=True)
    reciever = FetchUserSerializer(read_only=True)

    class Meta:
        model = Transmission
        fields = '__all__'
