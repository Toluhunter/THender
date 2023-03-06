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


def set_name(model, filename):
    extension = filename.split(".")[-1]
    filename = os.path.join("profile-picture", f"{model.username}-{model.id}.{extension}")

    return filename


class Account(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(
        primary_key=True,
        default=uuid4
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

    first_name = models.CharField(
        null=False,
        blank=False,
        max_length=70
    )

    last_name = models.CharField(
        null=False,
        blank=False,
        max_length=70
    )

    profile_picture = models.ImageField(null=True, blank=True, upload_to=set_name)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    def save(self, *args, **kwargs):

        self.full_clean()
        return super().save(*args, **kwargs)
