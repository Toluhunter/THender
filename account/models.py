import os
from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

class CustomUserManager(BaseUserManager):

    def create_user(self, username, password, email, **other_fields):

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **other_fields)

        user.set_password(password)

        user.save()

        return user
    
    def create_superuser(self, username, password, email, **other_fields):

        other_fields.setdefault("active", True)

        return self.create_user(username, password, email, **other_fields)
    

def set_name(model, *args):
    filename = os.path.join("media", "profile-picture", f"{model.username}-{model.id}")

    return filename

class Account(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(
        unique=True, 
        primary_key=True, 
        null=False,
        blank=True
        )

    username = models.CharField(
        max_length=40, 
        unique=True, 
        null=False, 
        blank=False,
        validators=[UnicodeUsernameValidator]
        )
    
    email = models.EmailField(
        null=False,
        unique=True,
        blank=False
        )

    profile_picture = models.ImageField(null=True, upload_to=set_name)


    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    
    def generate_id(self):
        id = uuid4()

        while Account.objects.filter(id=id).exists():
            id = uuid4()
        
        return id

    def save(self, *args, **kwargs):

        if not self.id:
            self.id = self.generate_id()
            
        self.full_clean()
        return super().save(*args, **kwargs)