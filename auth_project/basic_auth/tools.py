from django.contrib.auth import authenticate, get_user_model

from basic_auth.models import UserVerificationToken, PasswordResetToken
from common.tools import queue_email
from config.basic_auth_config import EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS, PASSWORD_RESET_TOKEN_EXPIRY_HOURS
from config.email_config import EMAIL_VERIFICATION_URL_TEMPLATE_STRING, EMAIL_VERIFICATION_EMAIL_TEMPLATE, \
    RESET_PASSWORD_EMAIL_TEMPLATE


def is_user_valid(email: str, password: str) -> bool:
    user = authenticate(email=email, password=password)
    if user is None or not user.is_verified:
        return False
    return True


def register_new_user(email: str, password: str) -> str or bool:
    user_model = get_user_model()

    user, was_created = user_model.objects.get_or_create(email=email)
    if not was_created:
        return "User with given email already exists"

    user.set_password(password)
    user.save()

    return None


def send_verification_email(email: str):
    user = get_user_model().objects.get(email=email)
    token = UserVerificationToken.objects.create(user=user)
    dispatch_verification_email(user.email, token.key)


def dispatch_verification_email(email: str, token: str):
    verification_url = EMAIL_VERIFICATION_URL_TEMPLATE_STRING.format(
        email_verification_token=token
    )
    subject = EMAIL_VERIFICATION_EMAIL_TEMPLATE["subject"]
    content = EMAIL_VERIFICATION_EMAIL_TEMPLATE["content"].format(
        link=verification_url,
        hours=EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS
    )
    queue_email(
        email=email,
        subject=subject,
        content=content,
    )


def is_valid_email_verification_token(token_key: str) -> bool:
    token = UserVerificationToken.objects.get(key=token_key)
    if token is None or not token.is_token_valid:
        return False
    return True


def is_valid_password_reset_token(email: str, token_key: str) -> bool:
    token = PasswordResetToken.objects.get(key=token_key)
    if token is None or token.user.email != email or token.is_token_valid:
        return False
    return True


def send_password_reset_email(email: str):
    user = get_user_model().objects.get(email=email)
    token = PasswordResetToken.objects.create(user=user)
    dispatch_password_reset_email(user.email, token.key)


def dispatch_password_reset_email(email: str, token: str):
    password_reset_url = RESET_PASSWORD_EMAIL_TEMPLATE.format(
        password_reset_token=token
    )
    subject = RESET_PASSWORD_EMAIL_TEMPLATE["subject"]
    content = RESET_PASSWORD_EMAIL_TEMPLATE["content"].format(
        link=password_reset_url,
        hours=PASSWORD_RESET_TOKEN_EXPIRY_HOURS
    )
    queue_email(
        email=email,
        subject=subject,
        content=content,
    )


def reset_user_password(email: str, password: str):
    user = get_user_model().objects.get(email=email)
    user.set_password(password)
    user.save()


def verify_user_by_verification_token(token_key):
    token = UserVerificationToken.objects.get(key=token_key)
    user = token.user
    user.is_verified = True
    user.save()
