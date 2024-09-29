from rest_framework import authentication
from knox.auth import TokenAuthentication as kox_auth
from rest_framework.authentication import TokenAuthentication as rest_auth
class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth=rest_auth().authenticate(request)
        if not auth:
            auth=kox_auth().authenticate(request)
            return auth
        return auth