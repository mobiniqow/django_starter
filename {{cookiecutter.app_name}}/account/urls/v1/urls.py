from django.urls import path
from account.urls.v1.views import (
    RegisterAPIView,
    LoginAPIView,
    ProfileAPIView,
    VerifyAPIView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = "v1"
urlpatterns = [
    path("verify/", VerifyAPIView.as_view(), name="verify"),
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
