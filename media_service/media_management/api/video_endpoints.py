from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from media_management.authentication import JWTAuthentication
from media_management.serializers import VideoSerializer
from media_management.models import Video
from media_management.permissions import IsVideoOwner
from media_management.publisher import publish_video_reverse_convert
from django.conf import settings
import os
import uuid


class UploadVideoView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VideoSerializer

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user.payload.get("user_id"))

        
class UserVideosView(generics.ListAPIView):
    
    serializer_class = VideoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        owner_id = self.request.user.payload.get("user_id")
        return Video.objects.filter(owner_id=owner_id)


class ReverseVideoView(generics.UpdateAPIView):
    
    serializer_class = VideoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        video = get_object_or_404(Video, id=kwargs["pk"])
        
        original_path = video.file.path 
        ext = os.path.splitext(original_path)[1]
        unique_name = f"{uuid.uuid4().hex}_reversed{ext}"
        output_path = os.path.join(os.path.dirname(original_path), unique_name)
        
        publish_video_reverse_convert(
            video_path=original_path,
            output_path=output_path,
            operation="reverse"
        )

        new_video = Video.objects.create(
            title=f"{video.title} (Reversed)",
            file=output_path.replace(settings.MEDIA_ROOT + "/", ""),
            owner_id=request.user.payload.get("user_id")
        )

        return Response(self.get_serializer(new_video).data, status=status.HTTP_202_ACCEPTED)

    
