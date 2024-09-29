from rest_framework import serializers
from . import models
from user_app.miniserializers import UserSerializerMini
from chat_in_group.miniserializers import CommunityChatSaveSerializer


class GroupCallSerializer(serializers.ModelSerializer):
    caller=serializers.SerializerMethodField("getCaller")
    community=serializers.SerializerMethodField("getCommunity")
    class Meta:
        model=models.GroupCall
        fields="__all__"
    def getCaller(self,model):
        return UserSerializerMini(model.caller).data
    def getCommunity(self,model):
        return CommunityChatSaveSerializer(model.community).data

class GroupCallMemberSerializer(serializers.ModelSerializer):
    groupCall=serializers.SerializerMethodField("getGroupCall")
    class Meta:
        model=models.GroupCallMember
        fields="__all__"
    def getGroupCall(self,model):
        return GroupCallSerializer(model.groupCall).data

class GroupCallSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.GroupCall
        fields="__all__"

class GroupCallMemberSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.GroupCallMember
        fields="__all__"
