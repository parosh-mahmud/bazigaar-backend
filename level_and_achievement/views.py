from rest_framework import generics
from . import models
from . import serializers
from rest_framework.response import Response
from django.contrib.auth import  get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.db.models import Q
from level_and_achievement.achivement_dict import achivement_dict

@api_view(["POST"])
def createUserLevel(request):
    user=request.user
    userlevel=models.UserLevel.objects.filter(user=user)
    if userlevel.exists():
        return Response({})
    else:
        userlevel=models.UserLevel()
        userlevel.user=user
        userlevel.save()
    return Response({})

@api_view(["GET"])
def getAllAchievements(request):
    queryset=models.Achievement.objects.all()
    count=queryset.count()
    if count<=0:
        for achivement in achivement_dict:
            ac=models.Achievement()
            ac.name=achivement["name"]  
            ac.description=achivement  ["description"]
            ac.points=achivement  ["points"]
            ac.save()
            
        queryset=models.Achievement.objects.all()
    print(queryset)
    return Response(serializers.AchievementSerializer(queryset,many=True).data) 

@api_view(["POST"])
def getAllUserAchievements(request):
    queryset=models.UserAchievement.objects.filter(user=request.user)
    return Response(serializers.UserAchievementSerializer(queryset,many=True).data) 

@api_view(["POST"])
def claimPoints(request):
    user=request.user
    achievementId=request.data.get("achievementId",None)
    any=models.UserAchievement.objects.filter(Q(user=user)&Q(achievement__id=achievementId))
    if not any.exists():
        return Response({"error":"Invalid"},status=400) 
    ua=any[0]
    userlevel=user.user_level
    userlevel.points+=ua.achievement.points
    userlevel.save()
    ua.claimed=True;
    ua.save()
    return Response(userlevel.data(),status=200) 

