from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
from chat_with_friend.models import ChatWithFriend
from base.base import SerializedModel

class Call(models.Model,SerializedModel):  
    caller=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="call_from_callers")
    videoOn=models.BooleanField(default=False)
    active=models.BooleanField(default=True)
    duration=models.CharField(max_length=56,blank=True)
    #pending, accepted , rejected , raised, ended , inAnotherCall
    CALL_CHOICES=[
        ('pending','pending'),
        ('accepted','accepted'),
        ('rejected','rejected'),
        ('raised','raised',),
        ('ended','ended'),
        ('inAnotherCall','inAnotherCall'),
    ]
    status=models.CharField(max_length=56,default="pending",choices=CALL_CHOICES) 
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    callee=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="call_from_callees")
    chat_with_friend=models.ForeignKey(ChatWithFriend,on_delete=models.CASCADE,null=True,related_name="calls",related_query_name="call")
