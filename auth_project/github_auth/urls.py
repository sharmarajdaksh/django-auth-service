from django.urls import path

from github_auth.views import OAuthLoginURLView, OAuthAuthorizeView

app_name = "github_auth"

urlpatterns = [
    path('oauth_login_url/', OAuthLoginURLView.as_view(), name="github_oauth_login_url"),
    path('oauth_authorize/', OAuthAuthorizeView.as_view(), name="github_oauth_authorize"),
]
