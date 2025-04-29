from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework import permissions
from accounts.models import CustomUser
from accounts.serializers import UserSerializer, CompleteProfileSerializer, UserInfoSerializer


class SignupView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = []
    serializer_class = UserSerializer


class CompleteProfileView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CompleteProfileSerializer
    
    def get_object(self):
        return self.request.user


class UserInfoView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user
