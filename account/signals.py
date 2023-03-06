from django.db.models.signals import pre_delete, post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from peer.models import Peer

Account = get_user_model()


@receiver(pre_delete, sender=Account)
def delete_profile_pic(sender, instance, **kwargs):
    if instance.profile_picture:
        instance.profile_picture.delete()


@receiver(post_save, sender=Account)
def create_peer_instance(sender, instance, created, **kwargs):
    if created:
        Peer.objects.create(owner=instance)
