from media_management.views import UploadVideoView, UserVideosView, ReverseVideoView
from django.urls import path

urlpatterns = [
    path("upload-video/", UploadVideoView.as_view(), name="upload-video"),
    path("user-videos/", UserVideosView.as_view(), name="user-videos"),
    path("reverse-video/<int:pk>/", ReverseVideoView.as_view(), name="reverse-video"),
]
