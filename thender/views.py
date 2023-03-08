from rest_framework import generics, status
from rest_framework.response import Response


class HealthCheckView(generics.GenericAPIView):

    def get(self, request):
        return Response("Healthy", status=status.HTTP_200_OK)
