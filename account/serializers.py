from uuid import uuid4

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers


User = get_user_model()

class CreateAccountSerializer(serializers.ModelSerializer):

    def __init__(self, instance=None, data=None, **kwargs):
        super().__init__(instance, data, **kwargs)

        self.fields["password"].write_only = True
    
    def validate(self, attrs):

        validate_password(attrs["password"])
        
        return attrs

    def create(self, validated_data):

        return self.Meta.model.objects.create_user(
            **validated_data
        )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "profile_picture"
        ]

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "profile_picture"
        ]

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=40, required=True)
    password = serializers.CharField(max_length=100, required=True)

    def validate(self, attrs):

        user = authenticate(
            username=attrs["username"], 
            password=attrs["password"]
            )
        
        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        
        attrs["user"] = user

        return attrs