from rest_framework.generics import ListAPIView 
from rest_framework import generics
from . import serializers,models
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view 
from django.shortcuts import get_object_or_404
from django.contrib.auth import  get_user_model
from chat_in_group.models import CommunityChat
from chat_in_group.serializers import CommunityChatSerializer
from base.ws import *
from base.ws_send_data import ws_send_model_to_data

class GetChatList(ListAPIView):
    serializer_class=serializers.ChatWithFriendSerializerForList
    def get_queryset(self):
        user=self.request.user
        user.save()
        queryset=models.ChatWithFriend.objects.filter(
            Q(message_req_from=user)
            | Q(message_req_to=user)
        ).order_by("-update_at")
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        user=self.request.user
        queryset2 = CommunityChat.objects.filter(
            member__member=user
        )
        serializer2 = CommunityChatSerializer(queryset2, many=True)

        return Response({
            "chat":serializer.data,
            "groupchat":serializer2.data            
            })
    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GetCommunityChatList(ListAPIView):
    serializer_class=CommunityChatSerializer
    def get_queryset(self):
        user=self.request.user
        user.save()
        queryset=CommunityChat.objects.filter(
            member__member=user
        ).order_by("-update_at")
        return queryset
    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class GetChatMessageList(ListAPIView):
    serializer_class=serializers.MessageSerializer
    def get_queryset(self):
        user=self.request.user
        id=self.request.query_params.get("id",None)
        chat=get_object_or_404(models.ChatWithFriend,id=id)
        if not (chat.message_req_from==user or
        chat.message_req_to==user):
            return []
        queryset=models.Message .objects.filter(
        Q(chat_with_friend__id=id)
        ).order_by("-created_at")
        return queryset
    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



class CreateChatWithFriend(generics.CreateAPIView):
    queryset = models.ChatWithFriend.objects.all()
    serializer_class=serializers.ChatWithFriendSaveSerializer

    def create(self, request, *args, **kwargs):
        message_req_to=request.data['message_req_to']
        message_req_from=request.data['message_req_from']
        # print(request.user)
        dictData=dict(request.data)
        # print('files' in dictData)
        # print('reaction' in dictData)
        # print('text' in dictData)
        message=models.Message()
        message.user=request.user
        if 'text' in dictData:
            message.text_message=dictData['text'][0]               
        any= models.ChatWithFriend.objects.filter(
            (Q(message_req_to__id=int(message_req_to)) &
            Q(message_req_from__id=int(message_req_from))) |
            (Q(message_req_to__id=int(message_req_from)) &
            Q(message_req_from__id=int(message_req_to)))    )
        if any.exists():
            chat_with_friend=any[0]
            message.chat_with_friend=chat_with_friend
            chat_with_friend.save()
            message.save()
            if 'images' in dictData:
                images=dictData['images']
                message.message_type="Image"
                message.save()
                for im in images:
                    im_mess=models.ImageMessage()
                    im_mess.image=im
                    im_mess.message=message
                    im_mess.save()
                # print("Image"*199) 
            id1=message.chat_with_friend.message_req_from.id
            id2=message.chat_with_friend.message_req_to.id
            ws_send_model_to_data(id1,message)
            ws_send_model_to_data(id2,message)
            if not chat_with_friend.is_req_accepted:
                isAccept=models.ChatWithFriend.objects.filter(Q(message_req_to__id=int(message_req_from)) & Q(message_req_from__id=int(message_req_to))).exists()
                chat_with_friend.is_req_accepted =isAccept
            # save the ChatWIthFriend to show him on the top of other old chat
                chat_with_friend.save()
            serializer = serializers.ChatWithFriendSerializer(chat_with_friend,many=False )
            
            data=serializer.data
            return Response(data, status=200)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            chat_with_friend=serializer.save()
            message.chat_with_friend=chat_with_friend
            message.save()
            if 'images' in dictData:
                images=dictData['images']
                message.message_type="Image"
                message.save()
                for im in images:
                    im_mess=models.ImageMessage()
                    im_mess.image=im
                    im_mess.message=message
                    im_mess.save()
            id1=message.chat_with_friend.message_req_from.id
            id2=message.chat_with_friend.message_req_to.id
            ws_send_model_to_data(id1,message)
            ws_send_model_to_data(id2,message)
            headers = self.get_success_headers(serializer.data)
            serializer=serializers.ChatWithFriendSerializer(chat_with_friend)
            return Response(serializer.data, status=201, headers=headers)
    
@api_view(['POST'])
def chatMessageExistOrNot(request):
    user=request.user
    friend_id=int(request.data['friend_id'])
    any=models.ChatWithFriend.objects.filter((Q(message_req_to__id=user.id) & Q(message_req_from__id=friend_id)) |
                                         (Q(message_req_to__id=friend_id) & Q(message_req_from__id=user.id))
                                         )
    if any.exists():
        chat_with_friend=any[0]
        serializer = serializers.ChatWithFriendSerializer(chat_with_friend,many=False )
        return Response(serializer.data,status=200)
    return Response({"msg":"Not Found"},status=404)

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


class UpdateChatWithFriend(generics.UpdateAPIView):
    queryset = models.ChatWithFriend.objects.all()
    serializer_class=serializers.ChatWithFriendSaveSerializer


class GetChatWithFriend(generics.RetrieveAPIView):
    queryset = models.ChatWithFriend.objects.all()
    serializer_class=serializers.ChatWithFriendSerializer
    def get(self, request, *args, **kwargs):
        # print(request.user)
        return self.retrieve(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        isSeen=True
        id=request.data["id"]
        unseenMessages=models.Message.objects.filter(
            Q(chat_with_friend=id) & Q(is_seen=False)
        ).exclude(user=request.user)
        for unseenMessage in unseenMessages:
            unseenMessage.is_seen=True
            unseenMessage.save()
        return self.retrieve(request, *args, **kwargs)

@api_view(['POST'])
def getChatByQuery(request):
    friendId=request.data["friendId"]
    userId=request.user.id
    any=models.ChatWithFriend.objects.filter(
        Q(Q(message_req_to=friendId) & Q(message_req_from=userId)) |
        Q(Q(message_req_to=userId) & Q(message_req_from=friendId)) 
    )
    if len(any)==0:
        return Response({},status=404)
    return Response(serializers.ChatWithFriendSerializer(any[0],many=False).data)