from . import models
from rest_framework import serializers
from user_app.miniserializers import  UserSerializerMini

class FollowSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Follow
        fields='__all__'
class FollowSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField("getUser")
    follow_to=serializers.SerializerMethodField("getFollowTo")
    class Meta:
        model=models.Follow
        fields='__all__'
    def getUser(self,model:models.Follow):
        return  UserSerializerMini(model.user,many=False).data
    def getFollowTo(self,model:models.Follow):
        return  UserSerializerMini(model.follow_to,many=False).data