from django.db.models.signals import post_delete
from django.dispatch import receiver
from media_management.models import Video


@receiver(post_delete, sender=Video)
def delete_video_files(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)
