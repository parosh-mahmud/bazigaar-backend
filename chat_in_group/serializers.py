from rest_framework  import serializers
from . import models
from user_app.miniserializers import UserSerializerMini
from group_call.serializers import GroupCallMemberSerializer,GroupCallSerializer
from group_call.models import GroupCall,GroupCallMember

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Reaction
        fields='__all__'
        
class ImageMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ImageMessage
        fields='__all__'

class MessageSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Message
        fields='__all__'
        

class MessageSerializer(serializers.ModelSerializer):
    images=serializers.SerializerMethodField("get_images")
    reactions=serializers.SerializerMethodField("get_reactions")
    user=serializers.SerializerMethodField("get_user")
    
    class Meta:
        model=models.Message
        fields='__all__'
    def get_images(self,model:models.Message):
        images=models.ImageMessage.objects.filter(message=model)
        
        return ImageMessageSerializer(images,many=True).data
    def get_reactions(self,model:models.Message):
        reactions=models.Reaction.objects.filter(message=model)
        return ReactionSerializer(reactions,many=True).data
    def get_user(self,model:models.Message):
        return UserSerializerMini(model.user).data
 

class CommunityMemberSerializer(serializers.ModelSerializer):
    member=serializers.SerializerMethodField("get_member")
    class Meta:
        model=models.CommunityMember
        fields='__all__'
    def get_member(self,model:models.CommunityMember):
        return UserSerializerMini(model.member).data

class CommunityChatSerializer(serializers.ModelSerializer):
    messages=serializers.SerializerMethodField("get_messages")
    members=serializers.SerializerMethodField("get_members")
    groupcalls=serializers.SerializerMethodField("get_calls")

    class Meta:
        model=models.CommunityChat
        fields='__all__'
    def get_messages(self,model:models.CommunityChat):
        messages=models.Message.objects.filter(chat_in_community=model)
        return MessageSerializer(messages,many=True).data
    def get_members(self,model:models.CommunityChat):
        members=models.CommunityMember.objects.filter(community=model)
        return CommunityMemberSerializer(members,many=True).data
    def get_calls(self,model):
        calls=model.groupcalls.all().filter(active=True).filter(member__status="pending")
        return GroupCallSerializer(calls,many=True).data



class CommunityChatSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.CommunityChat
        fields='__all__'