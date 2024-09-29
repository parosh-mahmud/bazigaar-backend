from dj_rest_auth.registration.views import SocialLoginView


from allauth.socialaccount.providers.google.provider import GoogleProvider,OAuth2Provider
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth.client import OAuthClient

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
