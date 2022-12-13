from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from account.urls.v1.views import (
    VerifyAPIView,
    ProfileAPIView,
    RegisterAPIView,
    LoginAPIView,
)


class TestUrl(TestCase):
    def setUp(self) -> None:
        super().setUp()
        # self .client =

    def test_verify_url_resolve(self):
        url = reverse("account:v1:verify")
        self.assertEqual(resolve(url).func.view_class, VerifyAPIView)

    def test_profile_url_resolve(self):
        url = reverse("account:v1:profile")
        self.assertEqual(resolve(url).func.view_class, ProfileAPIView)

    def test_register_url_resolve(self):
        url = reverse("account:v1:register")
        self.assertEqual(resolve(url).func.view_class, RegisterAPIView)

    def test_login_url_resolve(self):
        url = reverse("account:v1:login")
        self.assertEqual(resolve(url).func.view_class, LoginAPIView)

    def test_token_refresh_url_resolve(self):
        url = reverse("account:v1:token_refresh")
        self.assertEqual(resolve(url).func.view_class, TokenRefreshView)

    def test_token_verify_url_resolve(self):
        url = reverse("account:v1:token_verify")
        self.assertEqual(resolve(url).func.view_class, TokenVerifyView)
