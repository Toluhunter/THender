from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


from .serializers import TransmissionSerializer
from .models import Transmission


class FetchTransmissionList(generics.ListAPIView):
    '''
    Returns List of Transmission Where the the user is either
    the sender or the reciever
    '''
    serializer_class = TransmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transmission.objects.filter(Q(sender=user) | Q(reciever=user))
