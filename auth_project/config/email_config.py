from config.global_config import BASE_URL

EMAIL_VERIFICATION_URL_TEMPLATE_STRING = \
    BASE_URL + "/verify_email/?email_verification_token={email_verification_token}"
RESET_PASSWORD_URL_TEMPLATE_STRING = \
    BASE_URL + "/reset_password/?password_reset_token={password_reset_token}"

EMAIL_VERIFICATION_EMAIL_TEMPLATE = {
    "subject": "AuthProject: Verify your email to complete registration",
    "content": ("Hi and welcome to AuthProject!<br/>"
                "As a last part of your registration, you need to confirm your email."
                "You can do so by simply clicking on the link below or copying it into a browser's address bar."
                "<br/><br/>"
                "{link}<br/><br/>"
                "The link will be valid for {hours} hours from it's dispatch.<br/><br/>"
                "Regards<br/>"
                "The AuthProject Team"
                )
}

RESET_PASSWORD_EMAIL_TEMPLATE = {
    "subject": "AuthProject: Request for password reset",
    "content": ("Seems like you wish you change your AuthProject password!<br/>"
                "If this request was made by you, all is good."
                "You can do so by simply clicking on the link below or copying it into a browser's address bar."
                "<br/><br/>"
                "{link}<br/><br/>"
                "The link will be valid for {hours} hours from it's dispatch.<br/>"
                "In case you did not make this request, you may simply ignore this email<br/><br/>"
                "Regards<br/>"
                "The AuthProject Team"
                )
}
