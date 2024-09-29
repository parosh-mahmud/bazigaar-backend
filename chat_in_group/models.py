from django.db import models
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from base.base import SerializedModel


class CommunityChat(models.Model,SerializedModel):
    name=models.CharField(max_length=63)
    thumbnail=ResizedImageField( upload_to="image/community/",blank=True, null=True,)
    description=models.TextField(max_length=511,blank=True)
    GROUP_CATEGORY = [
    ('Chating', 'Chating'),
    ('Audio Call', 'Audio Call'),
    ('Video Call', 'Video Call'),
    ]
    group_category=models.CharField( max_length=20, choices=GROUP_CATEGORY)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return "CommunityChat "+str(self.id)+" "+ self.group_category
        

class CommunityMember(models.Model,SerializedModel):
    MEMBER_TYPE = [
    ('Admin', 'Admin'),
    ('Member', 'Member'),]
    member_type=models.CharField(max_length=10,choices=MEMBER_TYPE)
    member=models.ForeignKey(get_user_model(),on_delete=models.PROTECT)
    community=models.ForeignKey(CommunityChat,on_delete=models.CASCADE,related_query_name="member")
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)


class Message(models.Model,SerializedModel):
    is_seen=models.BooleanField(default=False)
    time=models.DateTimeField(auto_now_add=True)
    MESSAGE_TYPE_CHOICES = [
    ('Text', 'Text'),
    ('Image', 'Image'),
    ('Audio', 'Audio'),
    ('Video', 'Video'),
    ('File', 'File'),
    ('Call', 'Call'),
    ]
    message_type=models.CharField(max_length=20,choices=MESSAGE_TYPE_CHOICES,default="Text")
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="community_message")
    text_message=models.TextField(max_length=1024)
    chat_in_community=models.ForeignKey(CommunityChat,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class ImageMessage(models.Model,SerializedModel):
    image=ResizedImageField( upload_to="image/message/",blank=True, null=True,)
    message=models.ForeignKey(Message,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

class Reaction(models.Model,SerializedModel):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="community_reactions")
    REACTION_TYPE_CHOICES=[
        ('angry','angry'),
        ('crying','crying'),
        ('innocent','innocent'),
        ('sad','sad'),
        ('smile','smile'),
        ('wow','wow'),
    ]
    reaction=models.CharField(max_length=20,choices=REACTION_TYPE_CHOICES)
    message=models.ForeignKey(Message,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
