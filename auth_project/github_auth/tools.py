from config.github_oauth_config import GITHUB_CLIENT_ID, GITHUB_OAUTH_REDIRECT_URL


def get_github_oauth_login_url():
    return "https://github.com/login/oauth/authorize?" \
           f"client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_OAUTH_REDIRECT_URL}"
