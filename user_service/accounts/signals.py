from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import CustomUser
from .publisher import publish_user_deleted


@receiver(post_delete, sender=CustomUser)
def on_user_deleted(sender, instance, **kwargs):
    publish_user_deleted(instance.id)
