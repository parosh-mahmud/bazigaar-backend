from . import models
from rest_framework import serializers
from user_app.miniserializers import  UserSerializerMini

class CommentSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField("getUser")
    class Meta:
        model=models.Comment
        fields="__all__"
    def getUser(self,model:models.Comment):
        return UserSerializerMini(model.user,many=False).data
class CommentSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Comment
        fields="__all__"

class LiveStreamMiniSerializers(serializers.ModelSerializer):
    # url=serializers.SerializerMethodField("getUrl")
    started_ago_sec=serializers.SerializerMethodField("startedAgo")
    class Meta:
        model=models.LiveStream
        exclude=['host','started_at','created_at']
    # def getUrl(self,model:models.LiveStream):
        # return model.videoUrl()
    def startedAgo(self,model):
        return 302

class LiveStreamSaveSerializers(serializers.ModelSerializer):
    class Meta:
        model=models.LiveStream
        fields="__all__"
class LiveStreamSerializers(serializers.ModelSerializer):
    url=serializers.SerializerMethodField("getUrl")
    host=serializers.SerializerMethodField("getHost")
    started_ago_sec=serializers.SerializerMethodField("startedAgo")
    comments=serializers.SerializerMethodField("getComments")
    class Meta:
        model=models.LiveStream
        fields="__all__"
    def getHost(self,model):
        return UserSerializerMini(model.host,many=False).data
    def startedAgo(self,model):
        return 302
    def getUrl(self,model:models.LiveStream):
        return model.videoUrl()
    def getComments(self,model:models.LiveStream):
        comments=models.Comment.objects.filter(live_stream=model)
        return CommentSerializer(comments,many=True).data
    