from django.shortcuts import render
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.admin import TokenAdmin,Token
from rest_framework import generics, status
from django.contrib.auth import get_user_model, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from .serializers import *
from rest_framework.views import APIView
from wallet_app.models import Wallet
# Create your views here.


class AdminLoginView(APIView):
    permission_classes = (AllowAny,)
    def get_hello_world(self, request):
        return Response({"message": "Hello, World!"})
    
    def post(self, request:Request, format=None):
        # print(request.data["email"])
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
        
        
        if user_obj.is_staff == False:
            return Response({"type":"error","msg":"No admin record found."})
        
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

        try:
            User = get_user_model()
            curruser = User.objects.get(username=user_obj.username)
            wallet = Wallet.objects.get(user=curruser)
            dd["wallet_id"] = wallet.wallet_id
            dd["email"] = curruser.email
        except Wallet.DoesNotExist:
            User = get_user_model()
            curruser = User.objects.get(username=user_obj.username)
            wallet = Wallet.objects.create(user=curruser)
            dd["wallet_id"] = wallet.wallet_id
            dd["email"] = curruser.email
            pass

        return Response(data=dd,)
