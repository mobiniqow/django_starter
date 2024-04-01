from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User
from account.throttles import TwentyPerHourThrottle, FiftyPerDay, SevenPerMinuteThrottle
from account.urls.v1.serializers import (
    VerifySerializer,
    ProfileSerializer,
    UserRegisterSerializer,
    LoginSerializer,
    GeneralSerializer,
    TokenSerializer,
)
from account.send_sms import send_otp_message
from rest_framework import status


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class ProfileAPIView(GenericAPIView):
    serializer_class = ProfileSerializer

    @swagger_auto_schema(responses={200: ProfileSerializer()})
    def get(self, request):
        """
        get self profile
        """
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """
        update  user partiality
        """
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class VerifyAPIView(GenericAPIView):
    serializer_class = VerifySerializer
    throttle_classes = [SevenPerMinuteThrottle, TwentyPerHourThrottle, FiftyPerDay]

    @swagger_auto_schema(
        responses={200: TokenSerializer(many=True), 404: GeneralSerializer()}
    )
    def post(self, request):
        """
        verify user phone by sending otp code
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get("phone")
        user = get_object_or_404(User, phone=phone)
        if user.check_password(serializer.validated_data.get("password")):
            user.state = User.State.ACTIVE
            user.save()
            serializer = TokenSerializer(get_tokens_for_user(user))
            return Response(serializer.data)
        else:
            serializer = GeneralSerializer({"message": "wrong code"})
            return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    throttle_classes = [SevenPerMinuteThrottle, TwentyPerHourThrottle, FiftyPerDay]

    @swagger_auto_schema(responses={200: GeneralSerializer()})
    def post(self, request):
        """
        login user by phone number
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get("phone")
        user = User.objects.filter(phone=phone)
        otp = User.objects.make_random_password(length=4, allowed_chars="123456789")
        if not user.exists():
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User(**serializer.data)
            send_otp_message(user.phone, otp)
            user.set_password(otp)
            user.save()
            serializer = GeneralSerializer({"message": "code sending to your phone"})
            return Response(serializer.data)
        else:
            user = user.first()
            user.set_password(otp)
            send_otp_message(phone, otp)
            user.save()
            serializer = GeneralSerializer({"message": "code sending to your phone"})
            return Response(serializer.data)
