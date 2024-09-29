from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Follow
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models, serializers
from django.utils.timezone import datetime
from django.contrib.auth import  get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from notifications.models import RequestNotification
from notifications.serializers import RequestNotificationSaveSerializer

# Create your views here.

@api_view(['POST'])
def follow_to(request):
    user=request.user
    follow_id=request.data['follow_id']
    print(follow_id)
    print(request.user.id)
    _follow_to=get_object_or_404(get_user_model(),id=follow_id )
    follows=Follow.objects.filter(
        Q( user=user ) & Q(follow_to=_follow_to)
    )
    isFollowBack=Follow.objects.filter(
        Q( user=_follow_to ) & Q(follow_to=user)
    ).exists()
    
    if(isFollowBack):
        request_notification_data=    {
            "notification_to": follow_id,
            "notification_from": user.id,
            "notification_type": "follow_back",
            "extended_text": "_",
        }
    else:
        request_notification_data=    {
            "notification_to": follow_id,
            "notification_from": user.id,
            "notification_type": "follow_start",
            "extended_text": "_",
        }
    
    if follows.exists():
        if follows[0].active==False:
            follows.update(active=True)
            not_ser=RequestNotificationSaveSerializer(data=request_notification_data)
            if(not_ser.is_valid(raise_exception=True)):
                not_ser.save()
        return Response({"msg":"Successfully Followed"},status=200)
    else:    
        data={
            "user":user.id,
            "follow_to":follow_id
            }
        serializer=serializers.FollowSaveSerializer(data=data,partial=True)
        if(serializer.is_valid(raise_exception=False)):
            serializer.save()
            not_ser=RequestNotificationSaveSerializer(data=request_notification_data)
            if(not_ser.is_valid(raise_exception=True)):
                not_ser.save()
            return Response({"msg":"Successfully Followed"},status=201)
        return Response({"msg":"Follow is not successful"},status=404)

@api_view(['POST'])
def unfollow_to(request):
    user=request.user
    follow_id=request.data['unfollow_id']
    _follow_to=get_object_or_404(get_user_model(),id=follow_id )
    follows=Follow.objects.filter(
        Q( user=user ) & Q(follow_to=_follow_to)
    )
    if not follows.exists():
        return Response({"msg":"Unfollow unsuccessful"},status=404)
    follow=follows[0]
    follow.active=False
    follow.save()
    return Response({"msg":"Unfollow successful"},status=200)

