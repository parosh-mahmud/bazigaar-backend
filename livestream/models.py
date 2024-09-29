from collections.abc import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from base.base import SerializedModel
import uuid

class LiveStream(models.Model,SerializedModel):
    uid=models.UUIDField(
        default=uuid.uuid4,
        editable=False)
    thumbnail=ResizedImageField(upload_to="thumbnail",blank=True, null=True,)
    host=models.ForeignKey( get_user_model(),on_delete=models.CASCADE,related_name="live_streams",related_query_name="live_stream")
    name=models.CharField(max_length=56,)
    isLive=models.BooleanField(default=True)
    started_at=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    # schedule_date=models.DateTimeField()
    url=models.CharField(max_length=512,default="",blank=True)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        self.url=str(self.uid)
        return super().save(force_insert, force_update, using, update_fields)
        
    def videoUrl(self):
        return "https://moctobpltc-i.akamaihd.net/hls/live/571329/eight/playlist.m3u8"

class Reaction(models.Model,SerializedModel):
    live_stream=models.ForeignKey(LiveStream,on_delete=models.CASCADE)
    user=models.ForeignKey( get_user_model(),on_delete=models.CASCADE,related_name="reactions",related_query_name="reaction")
class Comment(models.Model,SerializedModel):
    text=models.CharField(max_length=255)
    user=models.ForeignKey( get_user_model(),on_delete=models.CASCADE,related_name="comments",related_query_name="comment")
    live_stream=models.ForeignKey(LiveStream,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)