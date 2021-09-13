from datetime import datetime, timedelta

from common.models import BaseToken
from config.basic_auth_config import EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS, PASSWORD_RESET_TOKEN_EXPIRY_HOURS


class UserVerificationToken(BaseToken):
    expiry_hours = EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS

class PasswordResetToken(BaseToken):
    expiry_hours = PASSWORD_RESET_TOKEN_EXPIRY_HOURS
