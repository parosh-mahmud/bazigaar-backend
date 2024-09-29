from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
class NewRegisterSerializer(RegisterSerializer):
    first_name=serializers.CharField()
    last_name=serializers.CharField()

    def custom_signup(self, request, user):
        user.first_name=request.data["first_name"]
        user.last_name=request.data["last_name"]
        try:
            user.src=request.data["src"]
        except:
            print('src not found')
        user.save()
