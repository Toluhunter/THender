from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


from .serializers import TransmissionSerializer, CreateTransmissionSerializer, HistorySerializer
from .models import Transmission, History
from .permissions import IsParticipant, IsReciever


class FetchTransmissionListView(generics.ListAPIView):
    '''
    Returns List of Transmission Where the the user is either
    the sender or the reciever
    '''
    serializer_class = TransmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transmission.objects.filter(Q(sender=user) | Q(reciever=user))


class AddTransmissionView(generics.CreateAPIView):
    '''
    View To Make Transmission File Request
    '''
    serializer_class = CreateTransmissionSerializer
    permission_classes = [IsAuthenticated]


class PendingTransmissionView(generics.ListAPIView):
    '''
    View to retrun transmissions that haven't been accepted
    '''
    serializer_class = TransmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transmission.objects.filter(reciever=self.request.user, accepted=False)


class FetchAcceptedTransmission(generics.ListAPIView):
    '''
    Returns List of accepted Transmission Where the the user is either
    the sender or the reciever
    '''
    serializer_class = TransmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transmission.objects.filter(Q(sender=user) | Q(reciever=user), accepted=True)


class DeleteTransmissionView(mixins.DestroyModelMixin, generics.GenericAPIView):

    permission_classes = [IsAuthenticated, IsParticipant]

    def get_object(self):
        id = self.kwargs["id"]
        obj = get_object_or_404(Transmission, id=id)
        self.check_object_permissions(request=self.request, obj=obj)

        return obj

    def delete(self, request, *args, **kwargs):

        transmission = self.get_object()
        History.objects.create(
            reciever=transmission.reciever,
            sender=transmission.sender,
            filename=transmission.file_name,
            start_date=transmission.start_date,
            status=History.FAILED
        )
        return self.destroy(request, *args, **kwargs)


class AcceptTransmisionRequest(generics.GenericAPIView):

    permission_classes = [IsAuthenticated, IsReciever]

    def get_object(self):
        id = self.kwargs["id"]
        transmission = get_object_or_404(Transmission, id=id)
        self.check_object_permissions(self.request, transmission)
        return transmission

    def get(self, request, *args, **kwargs):

        transmission = self.get_object()
        transmission.accepted = True
        transmission.save()

        return Response(TransmissionSerializer(instance=transmission).data, status=status.HTTP_200_OK)


class TransmissionHistoryView(generics.ListAPIView):
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return History.objects.filter(Q(reciever=user) | Q(sender=user))
