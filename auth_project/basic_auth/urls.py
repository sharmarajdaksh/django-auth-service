from django.urls import path

from basic_auth.views import LoginView, RegisterView, VerifyEmailView, ForgotPasswordView, ResetPasswordView

app_name = "basic_auth"

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('verify_email/', VerifyEmailView.as_view(), name="verify_email"),
    path('forgot_password/', ForgotPasswordView.as_view(), name="forgot_password"),
    path('reset_password/', ResetPasswordView.as_view(), name="reset_password"),
]
