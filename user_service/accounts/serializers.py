from rest_framework import serializers
from accounts.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ["id", "email", "password"]
        read_only_fields = ["id"]
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CompleteProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "profile_photo"]
        extra_kwargs = {
            'first_name': {"allow_blank": True, "required": False},
            'last_name': {"allow_blank": True, "required": False},
            'profile_photo': {"required": False}
        }


class UserInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "profile_photo", "created_at"]

