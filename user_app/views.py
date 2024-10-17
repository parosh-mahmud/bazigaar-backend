from rest_framework.decorators import api_view
import uuid
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from level_and_achievement.models import UserAchievement, Achievement
from rest_framework.response import Response
from . import models, serializers
from rest_framework import serializers as rst_serializers

from chat_with_friend.models import ChatWithFriend

from django.utils.timezone import datetime
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework import status
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ResendEmailVerificationView
from dj_rest_auth.views import PasswordResetConfirmView, PasswordResetView
from allauth.account.models import EmailAddress
import random
import string
from .login_serializers import CustomPasswordResetConfirmSerializer, CustomPasswordResetSerializer
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from level_and_achievement.models import UserAchievement, Achievement
from .serializers import UserUpdateSerializer
from base.ws import backend_token
from django.shortcuts import get_object_or_404


User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request, user_id):
    try:
        user = get_user_model().objects.get(id=user_id)
        return Response(
            {
                'user': serializers.UserSerializer(user, many=False).data,
                'cards': [
                    {"header": "Deposits", "value": 0},
                    {"header": "Withdrawals", "value": 0},
                    {"header": "Transactions", "value": 0},
                    {"header": "Total Buy Ticket", "value": 0},
                    {"header": "Total Win Ticket", "value": 0},
                    {"header": "Total Win Bonus", "value": user.bonusbgtoken},
                    {"header": "Total Referral", "value": 0},
                    {"header": "Balance", "value": user.bgcoin}
                ]

            }

        )
    except UserUpdateSerializer.Meta.model.DoesNotExist:
        return Response({'error': 'No user found with the given user_id'}, status=404)
    return Response()


@api_view(['POST'])
def getUser(request):
    user = request.user
    return Response(
        serializers.UserSerializer(user, many=False).data,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def ws_permission(request,pk,type):
    token=request.data.get("token",None)
    if not token:
        return Response({"permission":False,"ident":"None"},status=400)
    if token==backend_token:
        return Response({"permission":True,"ident":"server"})
    token_user=User.objects.filter(auth_token=token).first()
    if not token_user:
        return Response({"permission":False,"ident":"None"},status=400)
    if type=="listen":
        user=User.objects.filter(pk=pk).first()
        if user==token_user:
            return Response({"permission":True,"ident":f"user{pk}"})
    if type=="2v2Chat":
        chat=ChatWithFriend.objects.filter(pk=pk).first()
        if not chat:
            return Response({"permission":False,"ident":"None"})
        if chat.message_req_from==token_user or chat.message_req_to==token_user:
            return Response({"permission":True,"ident":f"user{token_user.pk}"})
        else:
            return Response({"permission":False,"ident":"None"})
    return Response(
       {"permission":False,"ident":"None"},status=400
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateUser(request, user_id):
    user = get_user_model().objects.get(id=user_id)
    serializer = serializers.UserSaveSerializer(
        user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"msg": "Update Successful"})
    else:
        return Response(serializer.errors)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    userdata = request.data.copy()
    print("request data:", userdata)
    profile_picture = userdata.get('profile_picture')
    profile_image = False
    try:
        profile_image = profile_picture[0]
    except Exception:
        pass

    if profile_image:
        # if isinstance(profile_picture[0], str) and '/media' in item:
        if not isinstance(profile_image, rst_serializers.ImageField):
            # Remove profile_picture if not an ImageField
            userdata.pop('profile_picture', None)
    print('cleanedup data', userdata)
    serializer = UserUpdateSerializer(user, data=userdata, partial=True)
    # print(user)
    # print(serializer)
    if serializer.is_valid():
        # Exclude fields that should not be updated
        serializer.save(bgcoin=user.bgcoin, bgtoken=user.bgtoken,
                        bonusbgtoken=user.bonusbgtoken)
        print(serializer.data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    print(request.data)
    serializer = serializers.UserSaveSerializer(
        user, data=request.data, partial=True)
    if serializer.is_valid():
        print("this is updated")
        model = serializer.save()
        data = serializers.UserSerializer(model, many=False).data
        print("this line")
        return Response(data)
    else:
        for key, error in serializer.errors.items():
            return Response({"error": error[0]}, status=400)
        return Response(serializer.errors, status=304)


@api_view(['POST'])
def update_last_online(request):
    user: models.User = request.user
    user.last_online = datetime.now()
    user.save()
    return Response({"msg": "success"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_user_by_search_name(request):
    q = request.data['q']
    users = get_user_model().objects.filter(
        Q(username__icontains=q) | Q(nickname__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)).exclude(id=request.user.id)  # .exclude(username="").exclude(nickname="")
    if users.count()>100:
        users=users[:100]
    return Response(serializers.UserSerializer(users, many=True).data)


class ProfilePictureUpdate(APIView):
    def post(self, request, format=None):
        try:
            user = request.user
        except:
            return Response({"type": "error", "msg": "user not found"})
        if get_user_model().objects.filter(username=user.username).exists():
            profile = get_user_model().objects.get(username=user.username)
            serializer = serializers. UserPictureSerializer(
                profile, data=request.data, partial=True)
        else:
            return Response({"type": "error", "msg": "Registered user not found"})
        if serializer.is_valid():
            serializer.save()
            return Response({"type": "Success", "msg": "Picture Updated", "New_image": serializer.data})
        else:
            return Response(serializer.errors)


@api_view(['POST'])
def exchangeCoinToToken(request):
    exchangeReqValue = int(request.data["coin"])
    try:
        bonus = int(request.data["bonus"])
    except:
        bonus = False
    user = request.user

    if user.bgcoin > exchangeReqValue:
        user.bgcoin -= exchangeReqValue
        user.bgtoken += exchangeReqValue
        if bonus:
            user.bgtoken += exchangeReqValue
        user.save()
        a = Achievement.objects.filter(
            name="Convert BGcoin into BGToken").first()
        ua = UserAchievement.objects.filter(
            achievement=a).filter(user=user).first()
        if a and not ua:
            ua = UserAchievement()
            ua.achievement = a
            ua.user = user
            ua.save()
        return Response({}, status=200)
    else:
        return Response({}, status=400)


@api_view(['POST'])
def changePassword(request):
    current_password = request.data["current_password"]
    password1 = request.data["new_password1"]
    password2 = request.data["new_password2"]
    user = request.user
    success = user.check_password(current_password)
    if (success):
        if password1 == password2:
            user.set_password(password1)
            user.save()
            return Response({"msg": "Password change successful"})
        return Response({"msg": "Password do not matches"})
    return Response({"msg": "You have given wrong password."})


class CustomVerifyEmailView(VerifyEmailView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        token = Token.objects.create(user=confirmation.email_address.user).key
        confirmation.delete()
        return Response({'detail': 'ok', "token": token}, status=status.HTTP_200_OK)


class CustomRegisterView(RegisterView):
    def post(self, request, *args, **kwargs):
        print("i am here for user registration--1")
        email = request.data["email"]
        print("i am here for user registration--2")
        any = get_user_model().objects.filter(email=email)
        if any.exists():
            user = any[0]
            email_address = EmailAddress.objects.get(user=user)
            if not email_address.verified:
                user.delete()
        refferal = request.data.get("refferal", None)

        a = Achievement.objects.filter(name="Refer a friend").first()
        user = get_user_model().objects.filter(ref=refferal).first()
        ua = UserAchievement.objects.filter(achievement=a).filter(user=user)
        if a and user and not ua:
            ua = UserAchievement()
            ua.achievement = a
            ua.user = user
            ua.save()
        return self.create(request, *args, **kwargs)


class CustomPasswordResetView(PasswordResetView):
    serializer_class = CustomPasswordResetSerializer


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    serializer_class = CustomPasswordResetConfirmSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def customPasswordResetView(request):
    obj = models.ResetPasswordModel()
    letters = string.ascii_uppercase
    code = ''.join(random.choice(letters + string.digits) for _ in range(6))
    obj.key = code
    obj.email = request.data["email"]
    obj.save()
    context = {
        "email": request.data["email"],
        "code": code,
        "protocol": "https",
    }
    subject = loader.render_to_string(
        "registration/password_reset_subject.html", context)
    # Email subject *must not* contain newlines
    subject = "".join(subject.splitlines())
    body = loader.render_to_string(
        "registration/password_reset_email.html", context)
    from_email = None
    html_email_template_name = "registration/password_reset_email.html"
    to_email = request.data["email"]
    email_message = EmailMultiAlternatives(
        subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, "text/html")

    email_message.send()
    return Response({"msg": "Email has been Sent"})

@api_view(["POST"])
@permission_classes([AllowAny])
def customPasswordResetConfirmView(request):
    code = request.data["code"]
    methodType = request.data["type"]
    if methodType == "verifyCode":
        obj = models.ResetPasswordModel.objects.filter(
            key=code).latest("created_at")
        email = obj.email
        user = get_user_model().objects.get(email=email)
        return Response({"verified": True})
    elif methodType == "setPassword":
        obj = models.ResetPasswordModel.objects.filter(
            key=code).latest("created_at")
        email = obj.email
        user = get_user_model().objects.get(email=email)
        password1 = request.data["password1"]
        password2 = request.data["password2"]
        if password1 == password2:
            user.set_password(password1)
            user.save()
            return Response({"msg": "Done"})
        else:
            return Response({"msg": "password Change failed"}, status=404)
    return Response({"msg": "failed"}, status=404)


# convert coin to token
@api_view(["POST"])
def convert_coin_to_token(request, amount):
    return Response("Coin converted to token")


@api_view(["POST"])
def setReferral(request):
    referred_user = request.user
    referrer_code = request.data.get("referrer_code", None)
    if not referrer_code:
        return Response({"msg": "No referrer_code found"}, status=400)
    referrer = User.objects.filter(ref=referrer_code).first()
    if not referrer:
        return Response({"msg": "No referrer found"}, status=400)
    try:
        referral = models.Referral()
        referral.referred_user = referred_user
        referral.referrer_code = referrer_code
        referral.referrer = referrer
        referrer.save()
    except Exception as e:
        return Response({"msg": f"Error : {e}"}, status=400)
    return Response({"msg": "Successful"}, status=200)

# request coin to reseller
# new model -> user id for both , amount , files
