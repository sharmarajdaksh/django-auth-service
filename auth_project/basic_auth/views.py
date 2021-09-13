from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_201_CREATED
from rest_framework.views import APIView

from basic_auth.serializers import LoginSerializer, RegisterSerializer, VerifyEmailSerializer, \
    ForgotPasswordSerializer, ResetPasswordSerializer
from basic_auth.tools import is_user_valid, register_new_user, send_verification_email, send_password_reset_email, \
    is_valid_email_verification_token, is_valid_password_reset_token, reset_user_password, \
    verify_user_by_verification_token
from common.tools import get_error_response, get_success_response, is_registered_email


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        if is_user_valid(email, password):
            return get_success_response(
                HTTP_200_OK,
                {
                    "authenticated": True,
                }
            )

        return get_error_response(HTTP_401_UNAUTHORIZED, ["Invalid username or password"])


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        registration_error = register_new_user(email=email, password=password)
        if registration_error is not None:
            return get_error_response(HTTP_403_FORBIDDEN, [registration_error])

        send_verification_email(email)

        return get_success_response(
            HTTP_201_CREATED,
            {
                "registered": True,
                "verified": False,
                "authenticated": True,
            }
        )


class VerifyEmailView(APIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["email_verification_token"]
        if not is_valid_email_verification_token(token):
            return get_error_response(
                HTTP_401_UNAUTHORIZED,
                ["Invalid email verification token"]
            )

        verify_user_by_verification_token(token)

        return get_success_response(
            HTTP_200_OK,
            {
                "verified": True,
                "message": "Email verified successfully",
            }
        )


class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        if not is_registered_email(email):
            return get_error_response(
                HTTP_401_UNAUTHORIZED,
                ["Given email is not associated with any account"]
            )

        send_password_reset_email(email)

        return get_success_response(
            HTTP_200_OK,
            {
                "message": "Password reset email dispatched",
            }
        )


class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        token = serializer.validated_data["password_reset_token"]
        password = serializer.validated_data["password"]

        if not is_valid_password_reset_token(email, token):
            return get_error_response(
                HTTP_401_UNAUTHORIZED,
                ["Invalid password reset token"]
            )

        reset_user_password(email, password)

        return get_success_response(
            HTTP_200_OK,
            {
                "message": "Password reset successfully",
            }
        )
