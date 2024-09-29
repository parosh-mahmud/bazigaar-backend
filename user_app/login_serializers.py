
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.urls import exceptions as url_exceptions

from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from django.urls import exceptions
from .serializers import *

class NewLoginSerializer(LoginSerializer):
    #username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_email(self, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = 'Must include "email" and "password".'
            raise exceptions.ValidationError(msg)

        return user
        


from dj_rest_auth.serializers import PasswordResetSerializer, PasswordResetConfirmSerializer

class CustomPasswordResetSerializer(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return PasswordResetForm
        
class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    @property
    def password_reset_form_class(self):
        return PasswordResetForm
        