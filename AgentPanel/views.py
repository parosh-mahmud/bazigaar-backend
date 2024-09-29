from django.shortcuts import render
from dj_rest_auth.serializers import LoginSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.admin import TokenAdmin,Token
from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import  get_user_model
from django.contrib.auth import login
from AdminPanel.serializers import *
from AdminPanel.views import AdminLoginView
from rest_framework.views import APIView

# Create your views here.


class AgentLoginView(APIView):

    # authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = permissions.AllowAny
    
    def post(self, request, format=None):
        try:
            email=request.data["email"]
            password=request.data["password"]
            if email == '':
                return Response({"type":"error","msg":"email not found."})
            if password == '':
                return Response({"type":"error","msg":"password not found."})
        except:
            return Response({"type":"error","msg":"email or password not found."})
        
        if get_user_model().objects.filter(email=email).exists():
            user_obj = get_user_model().objects.get(email=email)
        elif User.objects.filter(username=email).exists():
            user_obj = get_user_model().objects.get(username=email)
        else:
            return Response({"type":"error","msg":"Registered user not found."})
        

        if user_obj:
            if user_obj.check_password(password) == False:
                return Response({"type":"error","msg":"Password Incorrect."})
        else:
            return Response({"type":"error","msg":"username or email not found."})
        
        
        if user_obj.is_agent == False:
            return Response({"type":"error","msg":"No Agent record found."})
        
        credentials = {
            'username': user_obj.username,
            'password': password
        }
        serializer = AuthTokenSerializer(data=credentials)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        
        login(request, user)

        dd={}
        dd["username"] = user_obj.username
        dd["email"] = user_obj.email
        # Check if the user has a wallet
        Token.objects.get(user= user).delete()

        dd["token"] = Token.objects.create(user= user).key

        return Response(data=dd,)