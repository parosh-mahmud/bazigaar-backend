from django.db import models
from django.contrib.auth import get_user_model
from base.base import SerializedModel

class LudoGame(models.Model,SerializedModel):
    player1=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
    player2=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
    player3=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
    player4=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

class LudoGame2v2(models.Model,SerializedModel):
    player1=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
    player2=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
    player3=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
    player4=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

class LudoGameStartModel(models.Model,SerializedModel):
    player=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,)
    created_at=models.DateTimeField(auto_now_add=True)
    GAME_BOARD_CHOICES=(
        ("2","2"),
        ("3","3"),
        ("4","4"),
    )
    game_board=models.CharField(max_length=1,choices=GAME_BOARD_CHOICES)
    STATUS_CHOICES=(
        ("Searching","Searching"),
        ("Opponent Founded","Opponent Founded"),
        ("Game Started","Game Started"),
    )
    status=models.CharField(max_length=28,choices=STATUS_CHOICES)

