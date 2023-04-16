from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class HealthCheckView(generics.GenericAPIView):

    def get(self, request):
        return Response("OK", status=status.HTTP_200_OK)


class CheckTokenView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)
