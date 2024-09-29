from rest_framework import response
from . import models
from . import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, renderer_classes
from django.db.models import Q
from chat_with_friend.models import ChatWithFriend


@api_view(('GET',))
def socket(request):
    return response.Response({"":""})


@api_view(('POST',))
def startCall(request):
    user:get_user_model()=request.user
    # create call
    call=models.Call()
    call.caller=user
    call.callee=get_user_model().objects.get(id=request.data["callee"])
    chat_with_friend=get_object_or_404(ChatWithFriend,id=request.data["chat_id"])
    call.chat_with_friend=chat_with_friend
    call.videoOn=request.data["videoOn"]
    call.save()
    serializer=serializers.CallSerializer(call,many=False)
    return response.Response(serializer.data)

@api_view(('POST',))
def rejectCall(request):
    call=get_object_or_404(models.Call,id=request.data["call_id"])
    call.status="rejected"
    call.active=False
    call.save()
    return response.Response({"msg":"Call Rejected"})

@api_view(('POST',))
def acceptCall(request):
    call=get_object_or_404(models.Call,id=request.data["call_id"])
    call.status="accepted"
    call.save()
    return response.Response({"msg":"Call Rejected"})
@api_view(('POST',))
def raisedCall(request):
    call=get_object_or_404(models.Call,id=request.data["call_id"])
    call.status="raised"
    call.save()
    return response.Response({"msg":"Call Rejected"})

@api_view(('POST',))
def endCall(request):
    call=get_object_or_404(models.Call,id=request.data["call_id"])
    call.active=False
    call.save()
    return response.Response({"msg":"Call Rejected"})

# @api_view(('POST',))
# def getCall(request):
#     call=get_object_or_404(models.Call,id=request.data["call_id"])
#     serializer=serializers.CallSerializer(call,many=False)
#     return response.Response(serializer.data)