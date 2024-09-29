from rest_framework import serializers
from . import models

class CommunityChatSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.CommunityChat
        fields='__all__'