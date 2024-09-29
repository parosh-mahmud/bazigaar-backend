from django.db import models
from django.contrib.auth import  get_user_model
from base.base import SerializedModel

# Create your models here.
class SpinningBatch(models.Model,SerializedModel):
    batchTime=models.DateTimeField(unique=True)
    onGoingBatch=models.BooleanField(default=True)
    winField=models.CharField(max_length=3,null=True)
    winAmount=models.IntegerField(null=True)

class Bid(models.Model,SerializedModel):
    bidChoices=(
        ("2x","2x"),
        ("4x","4x"),
        ("6x","6x"),
    )
    bidType=models.CharField(
        max_length=3,
        default="2x",
        choices=bidChoices
    )
    bidder=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    batch=models.ForeignKey(SpinningBatch,on_delete=models.CASCADE)
    amount=models.IntegerField()
    win=models.BooleanField(default=False)
