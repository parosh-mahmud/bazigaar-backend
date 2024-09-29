from django.db import models
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from base.base import SerializedModel

class ChatWithFriend(models.Model,SerializedModel):
    message_req_from=models.ForeignKey(get_user_model(),on_delete=models.PROTECT,related_name="chat_with_friend_req_from")
    message_req_to=models.ForeignKey(get_user_model(),on_delete=models.PROTECT,related_name="chat_with_friend_req_to")
    is_req_accepted=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.message_req_from)+" "+str(self.message_req_to)

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
    user=models.ForeignKey(get_user_model(),on_delete=models.PROTECT,related_name="message",null=True)
    text_message=models.TextField(max_length=1024,null=True)
    chat_with_friend=models.ForeignKey(ChatWithFriend,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)



 
class ImageMessage(models.Model,SerializedModel):
    image=ResizedImageField( upload_to="image/message/",blank=True, null=True,)
    message=models.ForeignKey(Message,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)


class Reaction(models.Model,SerializedModel):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="chat_with_friend_reactions")
    REACTION_TYPE_CHOICES=[
        ('angry','angry'),
        ('crying','crying'),
        ('innocent','innocent'),
        ('sad','sad'),
        ('smile','smile'),
        ('wow','wow'),
    ]
    reaction=models.CharField(max_length=20, choices=REACTION_TYPE_CHOICES)
    message=models.ForeignKey(Message,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
