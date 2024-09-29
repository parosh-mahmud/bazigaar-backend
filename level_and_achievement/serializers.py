from rest_framework import serializers
from . import models

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Achievement
        fields="__all__"


class UserLevelSerializer(serializers.ModelSerializer):
    currentLevel=serializers.SerializerMethodField("getCurrentLevel")
    class Meta:
        model=models.UserLevel
        fields="__all__"
    def getCurrentLevel(self,model):
        return model.currentLevel()
    
class UserAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.UserAchievement
        fields="__all__"