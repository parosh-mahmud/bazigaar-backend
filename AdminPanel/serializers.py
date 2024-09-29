from rest_framework import serializers
from user_app.models import *
from follow.models import Follow
from follow.serializers import FollowSerializer
from django.db.models import Q


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        exclude=['password']

class UserSerializer(serializers.ModelSerializer):
    
    followers=serializers.SerializerMethodField("getfollowers")
    followings=serializers.SerializerMethodField("getfollowings")
    friends=serializers.SerializerMethodField("getfriends")
    
    class Meta:
        model= User
        exclude=['password']
        
    def getfollowers(self,model:User):
        followers=Follow.objects.filter(
            Q(active=True) & Q(follow_to=model)
        )
        return FollowSerializer(followers,many=True).data
    def getfollowings(self,model:User):
        followings=Follow.objects.filter(
            Q(active=True) & Q(user=model)
        )
        return FollowSerializer(followings,many=True).data
    def getfriends(self,model:User):
        followings=Follow.objects.filter(
            Q(active=True) & Q(user=model)
        )
        followers=Follow.objects.filter(
            Q(active=True) & Q(follow_to=model)
        )
        friends=[]
        if( followings.exists() and followers.exists() ):
            for f in followers:
                any=followings.filter(follow_to=f.user)
                if any.exists():
                    friends.append(any[0])
        return FollowSerializer(friends,many=True).data