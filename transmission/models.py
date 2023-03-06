from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Peer(models.Model):
    user = models.ManyToManyField(to=User, related_name="peers")


class Transmission(models.Model):

    def set_id(self):

        id = uuid4()
        while (Transmission.objects.filter(id=id).exists()):
            id = uuid4()

        return id

    id = models.UUIDField(null=False, primary_key=True)

    reciever = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        related_name="recieving"
    )

    sender = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        related_name="sending"
    )

    file_hash = models.CharField(max_length=256, null=False, blank=False)

    bytes_sent = models.PositiveBigIntegerField(null=False)

    total_size = models.PositiveBigIntegerField(null=False)

    def save(self, *args, **kwargs):

        self.id = self.set_id()

        return super().save(*args, **kwargs)


class History(models.Model):

    SENDING = 0
    SUCCESS = 1
    FAILED = -1

    choices = (
        (SENDING, "Sending"),
        (SUCCESS, "success"),
        (FAILED, "Failed")
    )

    id = models.UUIDField(null=False, primary_key=True)
    reciever = models.ForeignKey(
        to=User,
        null=True,
        related_name="recieved",
        on_delete=models.SET_NULL
    )
    sender = models.ForeignKey(
        to=User,
        null=True,
        related_name="sent",
        on_delete=models.SET_NULL
    )
    filename = models.CharField(max_length=80, null=False, blank=False)
    startdate = models.DateTimeField(auto_now_add=True, null=False)
    enddate = models.DateTimeField(null=True)
    status = models.SmallIntegerField(
        null=False,
        validators=[MaxValueValidator(1), MinValueValidator(-1)],
        default=SENDING
    )

    def set_id(self):

        id = uuid4()
        while (Transmission.objects.filter(id=id).exists()):
            id = uuid4()

        return id

    def save(self, *args, **kwargs):

        self.id = self.set_id()

        return super().save(*args, **kwargs)
