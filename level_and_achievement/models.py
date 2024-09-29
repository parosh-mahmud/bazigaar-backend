from django.db import models
from django.contrib.auth import get_user_model
import math
from base.base import SerializedModel
class UserLevel(models.Model,SerializedModel):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,related_name="user_level")
    level = models.IntegerField(default=1)
    minOfRange = models.IntegerField(default=0)
    maxOfRange = models.IntegerField(default=100)
    points = models.IntegerField(default=0)

    def currentLevel(self):
        if self.points < 0:
            return 0
        elif self.points <= 99:
            return 1
        else:
            level = 1
            self.maxOfRange=100
            self.minOfRange=0
            diff = self.maxOfRange
            while self.points >= self.maxOfRange :
                level += 1
                diff += diff
                self.minOfRange=self.maxOfRange
                self.maxOfRange=diff+self.maxOfRange
            self.level=level
            self.save()
            return level


class Achievement(models.Model,SerializedModel):
    name = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(max_length=1000,null=True,blank=True)
    points = models.IntegerField(default=10)

    def __str__(self):
        return self.name


class UserAchievement(models.Model,SerializedModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    claimed=models.BooleanField(default=False)
    date_achieved = models.DateTimeField(auto_now_add=True)
