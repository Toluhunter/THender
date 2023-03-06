from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from . import serializers

User = get_user_model()


class RegisterView(generics.CreateAPIView):

    serializer_class = serializers.CreateAccountSerializer


class LoginView(generics.GenericAPIView):

    serializer_class = serializers.LoginSerializer

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
    serializer_class = serializers.AccountSerializer

    def get_object(self):

        obj = self.request.user
        self.check_object_permissions(request=self.request, obj=obj)

        return obj


class ProfileView(generics.RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AccountSerializer

    def get_object(self):

        id = self.kwargs["id"]
        obj = get_object_or_404(User, id=id)

        self.check_object_permissions(request=self.request, obj=obj)

        return obj


class SearchUserView(generics.ListAPIView):

    serializer_class = serializers.FetchUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.request.GET.get("q", None)
        if not username:
            raise Http404("Invalid query")

        return User.objects.filter(username__icontains=username)


class FetchFriendView(generics.ListAPIView):
    pass
