from rest_framework import serializers
from . import models
from user_app import miniserializers
from django.db.models import Q
from django.utils.timezone import now
from calling_app2.models import Call
from calling_app2.serializers import CallSerializer

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Reaction
        fields='__all__'

class ImageMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ImageMessage
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
        return miniserializers.UserSerializerMini(model.user).data


class ChatWithFriendSerializer(serializers.ModelSerializer):
    messages=serializers.SerializerMethodField("get_messages")
    message_req_from=serializers.SerializerMethodField("get_message_req_from")
    message_req_to=serializers.SerializerMethodField("get_message_req_to")
    lastMessage=serializers.SerializerMethodField("get_lastMessage")
    isOnline=serializers.SerializerMethodField("get_isOnline")
    noOfNewMessage=serializers.SerializerMethodField("get_noOfNewMessage")
    
    class Meta:
        model=models.ChatWithFriend
        fields='__all__'
    def get_messages(self,model:models.ChatWithFriend):
        messages=models.Message.objects.filter(chat_with_friend=model).order_by('created_at')
        return MessageSerializer(messages,many=True).data
    def get_message_req_from(self,model:models.ChatWithFriend):
        return miniserializers.UserSerializerMini(model.message_req_from).data
    def get_message_req_to(self,model:models.ChatWithFriend):
        return miniserializers.UserSerializerMini(model.message_req_to).data
    def get_lastMessage(self,model):
        message=models.Message.objects.filter(chat_with_friend=model).latest('created_at')
        return MessageSerializer(message,many=False).data
    def get_isOnline(self,model):
        return True
    def get_noOfNewMessage(self,model):
        messages=models.Message.objects.filter(Q(chat_with_friend=model)&Q(is_seen=False))
        return len(messages)

class ChatWithFriendSerializerForList(serializers.ModelSerializer):
    message_req_from=serializers.SerializerMethodField("get_message_req_from")
    # messages=serializers.SerializerMethodField("get_messages")
    message_req_to=serializers.SerializerMethodField("get_message_req_to")
    lastMessage=serializers.SerializerMethodField("get_lastMessage")
    isOnline=serializers.SerializerMethodField("get_isOnline")
    noOfNewMessage=serializers.SerializerMethodField("get_noOfNewMessage")
    calls=serializers.SerializerMethodField("get_calls")
    
    class Meta:
        model=models.ChatWithFriend
        fields='__all__'
    # def get_messages(self,model:models.ChatWithFriend):
    #     messages=models.Message.objects.filter(chat_with_friend=model).order_by('created_at')
    #     return MessageSerializer(messages,many=True).data
    def get_message_req_from(self,model:models.ChatWithFriend):
        return miniserializers.UserSerializerMini(model.message_req_from).data
    def get_message_req_to(self,model:models.ChatWithFriend):
        return miniserializers.UserSerializerMini(model.message_req_to).data
    def get_lastMessage(self,model):
        message=models.Message.objects.filter(chat_with_friend=model).latest('created_at')
        return MessageSerializer(message,many=False).data
    def get_isOnline(self,model):
        return True
    def get_noOfNewMessage(self,model):
        messages=models.Message.objects.filter(Q(chat_with_friend=model),Q(is_seen=False))
        return len(messages)
    def get_calls(self,model):
        calls=model.calls.all().filter(active=True).filter(status="pending")
        
        return CallSerializer(calls,many=True).data

class ChatWithFriendSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ChatWithFriend
        fields="__all__"

# ChatWithFriend ended part


# Save Message Serilaizers

class MessageSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Message
        fields='__all__'

# Save Image Message Serializers

class ReactionSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Reaction
        fields='__all__'

# Save Reaction Message Serializers

class ImageMessageSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ImageMessage
        fields='__all__'
