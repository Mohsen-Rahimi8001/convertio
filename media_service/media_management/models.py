from django.db import models


def video_path_create(instance, filename):
    return f"user_{instance.owner_id}/{filename}"


class Video(models.Model):
    owner_id = models.CharField(null=False, blank=False)
    title = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to=video_path_create, null=False, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"user_{self.owner_id}/{self.title}"
