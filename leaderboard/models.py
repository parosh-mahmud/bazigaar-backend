from django.db import models
from django.contrib.auth import get_user_model
from base.base import SerializedModel

class Leaderboard(models.Model,SerializedModel):
    # All Time, This Week, This Month
    name = models.CharField(max_length=100,default="All Time")
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class LeaderboardEntry(models.Model,SerializedModel):
    leaderboard = models.ForeignKey(Leaderboard, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    score = models.IntegerField(default=0)# win in dollar
    rate=models.CharField(default="0",max_length=10)
    position=models.IntegerField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.score}'
