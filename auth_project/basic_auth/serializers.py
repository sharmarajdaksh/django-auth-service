from rest_framework import serializers
from rest_framework.serializers import ValidationError


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        if attrs["confirm_password"] != attrs["password"]:
            raise ValidationError("Given passwords do not match")

        return super().validate(attrs)


class VerifyEmailSerializer(serializers.Serializer):
    email_verification_token = serializers.CharField()

    def validate(self, attrs):
        email_verification_token = attrs["email_verification_token"]
        if email_verification_token is None:
            raise ValidationError("Invalid request. No email verification token found")

        return super().validate(attrs)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password_reset_token = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        if attrs["confirm_password"] != attrs["password"]:
            raise ValidationError("Given passwords do not match")

        return super().validate(attrs)
