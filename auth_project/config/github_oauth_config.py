import os

from config.global_config import BASE_URL

GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID", "")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET", "")
GITHUB_OAUTH_REDIRECT_URL = BASE_URL + "/auth/github/callback"
