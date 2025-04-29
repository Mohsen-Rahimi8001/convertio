from rest_framework.permissions import BasePermission
from media_management.models import Video


class IsVideoOwner(BasePermission):
    def has_permission(self, request, view):
        video_id = view.kwargs.get("pk")

        if not video_id:
            return False
        
        try:
            video = Video.objects.get(id=video_id)
            
        except Video.DoesNotExist:
            return False

        print(video.owner_id)
        print(request.user.payload.get("user_id"))

        return video.owner_id == request.user.payload.get("user_id")
