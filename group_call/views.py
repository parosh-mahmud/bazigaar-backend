from rest_framework.response import Response
from . import models
from . import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, renderer_classes
from django.db.models import Q
from chat_in_group.models import CommunityMember





@api_view(('POST',))
def createAGroupCall(request):
    communityId=request.data['communityId']
    videoOn=request.data["videoOn"]
    community=models.CommunityChat.objects.filter(id=communityId)[0]
    groupCall=models.GroupCall()
    groupCall.caller=request.user
    groupCall.community=community
    groupCall.videoOn=videoOn
    groupCall.active=True
    groupCall.save()
    communityMembers=CommunityMember.objects.filter(community=community)
    for eachMember in communityMembers:
        if eachMember.member==request.user:
            continue
        groupMember=models.GroupCallMember()
        groupMember.member=eachMember.member
        groupMember.groupCall=groupCall
        groupMember.save()
    serializer=serializers.GroupCallSerializer(groupCall,many=False)
    return Response(serializer.data)


@api_view(('POST',))
def acceptGroupCall(request):
    call_id=request.data["call_id"]
    member=models.GroupCallMember.objects.get(
        Q(member=request.user) & Q(groupCall__id=call_id)
    )
    member.status="accepted"
    member.save()
    return Response({})

@api_view(('POST',))
def raisedGroupCall(request):
    call_id=request.data["call_id"]
    member=models.GroupCallMember.objects.get(
        Q(member=request.user) & Q(groupCall__id=call_id)
    )
    member.status="raised"
    member.save()
    return Response({})
@api_view(('POST',))
def deniedGroupCall(request):
    call_id=request.data["call_id"]
    member=models.GroupCallMember.objects.get(
        Q(member=request.user) & Q(groupCall__id=call_id)
    )
    member.status="rejected"
    member.save()
    return Response({})
@api_view(('POST',))
def endedGroupCall(request):
    call_id=request.data["call_id"]
    member=models.GroupCallMember.objects.get(
        Q(member=request.user) & Q(groupCall__id=call_id)
    )
    member.status="ended"
    member.save()
    return Response({})