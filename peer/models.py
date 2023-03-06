from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Peer(models.Model):

    id = models.UUIDField(default=uuid4, primary_key=True)
    owner = models.OneToOneField(to=User, on_delete=models.CASCADE,
                                 related_name="peer", null=False, blank=False)
    peers = models.ManyToManyField(to=User, related_name="all_paired")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class PeerRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(to=User, null=False, blank=False,
                             on_delete=models.CASCADE, related_name="recieved_request")
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE,
                               null=False, blank=False, related_name="sent_request")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ('user_id', 'sender')
