from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Transmission(models.Model):

    id = models.UUIDField(null=False, primary_key=True, default=uuid4)

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

    file_location = models.TextField(null=False, blank=False, unique=True)
    file_hash = models.CharField(max_length=65, null=False, blank=False, unique=True)

    bytes_sent = models.PositiveBigIntegerField(null=False, blank=False, default=0)

    total_size = models.PositiveBigIntegerField(null=False, blank=False)

    accepted = models.BooleanField(default=False, null=False, blank=False)

    def save(self, *args, **kwargs):

        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.file_hash}{self.sender}{self.reciever}'


class Transfer(models.Model):
    id = models.OneToOneField(to=Transmission, primary_key=True, on_delete=models.CASCADE)
    sender = models.ForeignKey(to=User, null=True, blank=False,
                               default=None, on_delete=models.CASCADE, related_name="transfer_sending")
    reciever = models.ForeignKey(to=User, null=True, blank=False,
                                 default=None, on_delete=models.CASCADE, related_name="transfer_recieving")


class History(models.Model):

    SENDING = 0
    SUCCESS = 1
    FAILED = -1

    choices = (
        (SENDING, "Sending"),
        (SUCCESS, "success"),
        (FAILED, "Failed")
    )

    id = models.UUIDField(null=False, primary_key=True, default=uuid4)
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

    def save(self, *args, **kwargs):
        self.full_clean()

        return super().save(*args, **kwargs)


class Online(models.Model):
    '''
    Table To Store Users who are online
    '''

    user = models.OneToOneField(to=User, on_delete=models.CASCADE,
                                primary_key=True, related_name="online")
