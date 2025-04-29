from django.urls import path
from .views import SignupView, CompleteProfileView, UserInfoView


urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("complete-profile/", CompleteProfileView.as_view(), name="complete-profile"),
    path("user-info/", UserInfoView.as_view(), name="user-info"),
]