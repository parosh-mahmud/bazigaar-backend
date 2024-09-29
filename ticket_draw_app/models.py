from django.db import models
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
import uuid
from base.base import SerializedModel

def upload_to1(instance, filename):
    return 'image/prizeImage/{filename}'.format(filename=filename)
def upload_to2(instance, filename):
    return 'image/firstPrize/{filename}'.format(filename=filename)
def upload_to3(instance, filename):
    return 'image/secondPrize/{filename}'.format(filename=filename)
def upload_to4(instance, filename):
    return 'image/thirdPrize/{filename}'.format(filename=filename)
def upload_to5(instance, filename):
    return 'image/coverImage/{filename}'.format(filename=filename)

class Ticket(models.Model,SerializedModel):
    #edited here
    LotteryName = models.CharField(max_length=255,null=True)
    price=models.IntegerField()
    drawPriceAmount=models.IntegerField()
    numberOfWinner=models.IntegerField()
    # lotteryuuid=models.CharField(max_length=255,default=uuid.uuid4)
    lotteryuuid=models.CharField(max_length=255,null= True)
    # prizeImage=ResizedImageField(upload_to=upload_to1)
    # coverImage=ResizedImageField(upload_to=upload_to5,null=True,blank=True)
    # firstPrize=ResizedImageField(upload_to=upload_to2)
    # secondPrize=ResizedImageField(upload_to=upload_to3)
    # thirdPrize=ResizedImageField(upload_to=upload_to4)


    prizeImage=models.CharField(max_length=255,null=True)
    coverImage=models.CharField(max_length=255,null=True)
    firstPrize=models.CharField(max_length=255,null=True)
    secondPrize=models.CharField(max_length=255,null=True)
    thirdPrize=models.CharField(max_length=255,null=True)

    totalNumberOfTickets=models.IntegerField()
    type = models.CharField(max_length=20)
    
    firstPrizeName=models.CharField(max_length=56,null=True)
    secondPrizeName=models.CharField(max_length=56,null=True)
    thirdPrizeName=models.CharField(max_length=56,null=True)
    
    numberOfFirstWinner=models.IntegerField(default=1)
    numberOfSecondWinner=models.IntegerField(default=2)
    numberOfThirdWinner=models.IntegerField(default=3)
    
    bannerColor= models.CharField(max_length=56,null=True,blank=True)
    
    ticketSellOpeningTime= models.DateTimeField(auto_now_add=True)
    ticketSellClosingTime= models.DateTimeField(blank=True)
    
    drawStatus = models.CharField(max_length=300,null=True,blank=True)
    active = models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    
    firstPrizeDrawIsComplete=models.BooleanField(default=False)
    secondPrizeDrawIsComplete=models.BooleanField(default=False)
    thirdPrizeDrawIsComplete=models.BooleanField(default=False)

    def __str__(self) :
        return str(self.id)


class LuckyNumber(models.Model,SerializedModel):
    number=models.CharField(max_length=20)
    buyer=models.ForeignKey(get_user_model(),on_delete=models.PROTECT)
    ticket=models.ForeignKey(Ticket,on_delete=models.CASCADE)
    win=models.BooleanField(default=False)
    purchaseDate=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class TicketBuyHistory(models.Model,SerializedModel):
    ticket=models.ForeignKey(Ticket,on_delete=models.PROTECT)
    buyer=models.ForeignKey(get_user_model(),on_delete=models.PROTECT)
    purchaseDate=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    pickNumber=models.CharField(max_length=20)
    quantity=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class TicketWinner(models.Model,SerializedModel):
    luckyNumber=models.ForeignKey(LuckyNumber,on_delete=models.CASCADE)
    ticket=models.ForeignKey(Ticket,on_delete=models.CASCADE)
    position=models.IntegerField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
