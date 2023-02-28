from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework import status

from .serializers import AccountSerializer, LoginSerializer, CreateAccountSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):

    serializer_class = CreateAccountSerializer
    parser_classes = [MultiPartParser]


class LoginView(generics.GenericAPIView):

    serializer_class  = LoginSerializer

    def post(self, request):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user=user)

        response = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return Response(response, status=status.HTTP_200_OK)

        
class RetrieveUpdateView(generics.RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer

    def get_object(self):
        
        obj = self.request.user
        self.check_object_permissions(request=self.request, obj=obj)

        return obj

class ProfileView(generics.RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer

    def get_object(self):

        id = self.kwargs["id"]
        obj = get_object_or_404(User, id=id)

        self.check_object_permissions(request=self.request, obj=obj)

        return obj

class FetchFriendView(generics.RetrieveAPIView):
    pass