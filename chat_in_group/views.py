from rest_framework import generics
from . import serializers
from . import models
from rest_framework.response import Response
from django.contrib.auth import  get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.db.models import Q
from base.ws_send_data import *

class GetCommunityChats(generics.ListAPIView):
    queryset = models.CommunityChat.objects.all()
    serializer_class=serializers.CommunityChatSerializer

class GetCommunityChat(generics.RetrieveAPIView):
    queryset = models.CommunityChat.objects.all()
    serializer_class=serializers.CommunityChatSerializer



class CreateChatInGroup(generics.CreateAPIView):
    queryset = models.CommunityChat.objects.all()
    serializer_class=serializers.CommunityChatSaveSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chatCommunity=serializer.save()
        try:
            ids=dict(request.data)["membersId"]
            admin=models.CommunityMember()
            admin.community=chatCommunity
            admin.member_type='Admin'
            admin.member=request.user
            admin.save()
            for id in ids:
                member=models.CommunityMember()
                member.community=chatCommunity
                member.member_type='Member'
                member.member=get_object_or_404(get_user_model(),id=int(id))
                member.save()
        except Exception as e:
            print("because of the "+str(e)+"chat has been deleted")
            chatCommunity.delete()
            return Response({"msg":"internal server error"}, status=500, headers=headers)
        serializer=serializers.CommunityChatSerializer(chatCommunity,many=False)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class CreateGroupMessage(generics.CreateAPIView):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSaveSerializer
    def create(self, request, *args, **kwargs):
        data=dict(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message=serializer.save()
        
        if request.data['message_type']=="Image":
            print("59")
            images=data['images']
            print("61")
            print(images)
            message.message_type="Image"
            message.save()
            for im in images:
                im_mess=models.ImageMessage()
                im_mess.image=im
                im_mess.message=message
                im_mess.save()
            # id1=message.chat_with_friend.message_req_from.id
            # id2=message.chat_with_friend.message_req_to.id
            # ws_send_model_to_data(id1,message)
            # ws_send_model_to_data(id2,message)
        serializer=serializers.MessageSerializer(message,many=False)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


@api_view(['POST'])
def reactOnMessage(request):
    message=get_object_or_404(models.Message,id=request.data ['message_id'])
    any=models.Reaction.objects.filter(
        Q(user= request.user) & Q(message=message)
    )
    if any.exists():
        
        if any.filter(reaction=request.data ['reaction']).exists():
            any[0].delete()
            return Response({"msg":"react deleted"})
        else:
            rct=any[0]
            rct.reaction=request.data ['reaction']
            rct.save()
        return Response({"msg":"react updated"})
    
    reaction=models.Reaction()
    reaction.user=request.user
    reaction.reaction=request.data ['reaction']
    reaction.message=message
    reaction.save()
    return Response({"msg":"reacted"})


# class CreateReactionOnMessage(generics.CreateAPIView):
#     queryset = models.Reaction.objects.all()
#     serializer_class = serializers.ReactionSerializer
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=201, headers=headers)
