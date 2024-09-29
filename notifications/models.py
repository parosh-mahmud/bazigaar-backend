from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from base.base import SerializedModel
from base.ws import wsMessageToUser
import json
# Create your models here.
class RequestNotification(models.Model,SerializedModel):
    NOTIFICATION_CHOICES=(
        ('follow_start','started following you.'),
        ('comment','comment to your livestream.'),
        ('mention','mentioned you to '),
        ('follow_back','follow you back.'),
        ('request_for_coins','request for'),
    )

    notification_type=models.CharField( max_length=20,choices=NOTIFICATION_CHOICES)
    extended_text=models.CharField(max_length=30,default="")
    notification_to=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="request_notifications_to")
    notification_from=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="request_notifications_from")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objectRefId=models.CharField(max_length=20,null=True,blank=True)

    def save(self, *args, **kwargs):
        super().save( *args, **kwargs)
        # userid=self.notification_to.id
        # data=json.dumps({
        #     "type": "RequestNotification",
        #     "data":self.data()})
        # wsMessageToUser(userid,data)


def upload_to(instance, filename):
    return 'image/thumbnail/{filename}'.format(filename=filename)

class PromotionNotification(models.Model,SerializedModel):
    TYPE_CHOICES=(
        ('type1','type1'),
        ('type2','type2'),
        ('type3','type3'),
        ('type4','type4'),
    )
    title=models.CharField(max_length=100,)
    thumbnail=ResizedImageField( upload_to=upload_to,blank=True, null=True,)
    notification_to=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="promotion_notifications_to",null=True,default=None,blank=True)
    notification_from=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="promotion_notifications_from",null=True,default=None,blank=True)
    type=models.CharField(max_length=10,choices=TYPE_CHOICES,default="type1")# type1 , type2 , type3
    date=models.DateTimeField(null=True,blank=True,)
    to_all=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class GameNotification(models.Model,SerializedModel):
    TYPE_CHOICES=(
        ('type1','type1'), # Get your bonus
        ('type2','type2'), # view more
        ('type3','type3'), # play now
        ('type4','type4'),
    )
    title=models.CharField(max_length=100,)
    thumbnail=ResizedImageField( upload_to=upload_to,blank=True, null=True,)
    notification_to=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="game_notifications_to",null=True,default=None,blank=True)
    notification_from=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="game_notifications_from",null=True,default=None,blank=True)
    type=models.CharField(max_length=10,choices=TYPE_CHOICES,default="type2")# type1 , type2 , type3
    date=models.DateTimeField(null=True,blank=True,)
    to_all=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class EventNotification(models.Model,SerializedModel):
    TYPE_CHOICES=(
        ('type1','type1'),
        ('type2','type2'),
        ('type3','type3'),
        ('type4','type4'),
    )
    title=models.CharField(max_length=100,)
    thumbnail=ResizedImageField( upload_to=upload_to,blank=True, null=True,)
    notification_to=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="event_notifications_to",null=True,default=None,blank=True)
    notification_from=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="event_notifications_from",null=True,default=None,blank=True)
    type=models.CharField(max_length=10,choices=TYPE_CHOICES,default="type1")# type1 , type2 , type3
    date=models.DateTimeField(null=True,blank=True,)
    to_all=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

