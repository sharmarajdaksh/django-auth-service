from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from common.tools import get_success_response
from github_auth.tools import get_github_oauth_login_url


class OAuthLoginURLView(APIView):

    def get(self, request):
        github_oauth_login_url = get_github_oauth_login_url()

        return get_success_response(
            HTTP_200_OK,
            {
                "github_oauth_login_url": github_oauth_login_url
            }
        )


class OAuthAuthorizeView(APIView):

    def post(self, request):
        pass