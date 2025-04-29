from rest_framework import serializers
from media_management.models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ["id", "title", "file"]
        read_only_fields = ["id"]
        
    def create(self, validated_data):
        owner_id = validated_data.get("owner_id", None)
        title = validated_data.get("title", None)
        file = validated_data.get("file", None)

        video = Video.objects.create(owner_id=owner_id, title=title, file=file)
        
        return video

