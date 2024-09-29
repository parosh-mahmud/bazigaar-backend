from django.db import models
from django.contrib.auth import get_user_model
from chat_in_group.models import CommunityChat
from base.base import SerializedModel


class GroupCall(models.Model,SerializedModel):
    caller=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,)
    community=models.ForeignKey(CommunityChat,on_delete=models.CASCADE,null=True,related_name="groupcalls",related_query_name="groupcall")
    videoOn=models.BooleanField(default=False)
    active=models.BooleanField(default=True)
    duration=models.CharField(max_length=56,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class GroupCallMember(models.Model,SerializedModel):
    groupCall=models.ForeignKey(GroupCall,on_delete=models.CASCADE,related_name="members",related_query_name="member")
    member=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_query_name="group_member",related_name="group_members")
    #pending, accepted , rejected , raised, ended
    status=models.CharField(max_length=56,default="pending") 
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
