import uuid
from django_resized import ResizedImageField
from django.contrib.sites import requests
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from base.base import SerializedModel

def upload_to1(instance, filename):
    return 'media/image/prizeImage/{filename}'.format(filename=filename)


def upload_to2(instance, filename):
    return 'media/image/firstPrize/{filename}'.format(filename=filename)


def upload_to3(instance, filename):
    return 'media/image/secondPrize/{filename}'.format(filename=filename)


def upload_to4(instance, filename):
    return 'media/image/thirdPrize/{filename}'.format(filename=filename)


def upload_to5(instance, filename):
    return 'media/image/coverImage/{filename}'.format(filename=filename)


class Lottery(models.Model,SerializedModel):
    TYPE_CHOICES = (
        ('Regular', 'Regular'),
        ('Special', 'Special'),
        ('Other', 'Other'),
    )
    LotteryId = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    LotteryName = models.CharField(max_length=255, blank=True, null=True)
    Price = models.IntegerField(default=0)
    PriceAmount = models.IntegerField(default=0)
    NumberOfWinners = models.IntegerField(default=0)
    NumberOfTickets = models.IntegerField(default=0)
    OpeningTime = models.DateTimeField(blank=True)
    ClosingTime = models.DateTimeField(blank=True)
    FirstPrizeName = models.CharField(max_length=255, blank=True, null=True)
    SecondPrizeName = models.CharField(max_length=255, blank=True, null=True)
    ThirdPrizeName = models.CharField(max_length=255, blank=True, null=True)
    TotalFirstPrizeWinner = models.IntegerField(default=0)
    TotalSecondPrizeWinner = models.IntegerField(default=0)
    TotalThirdPrizeWinner = models.IntegerField(default=0)
    isOpen = models.BooleanField(default=True)
    isDrawComplete = models.BooleanField(default=False)
    # image_first = models.ImageField(max_length=255,upload_to=image_to_url,blank=True,null=True)
    # image_second = models.ImageField(max_length=255,upload_to=image_to_url,blank=True,null=True)
    # image_third = models.ImageField(max_length=255,upload_to=image_to_url,blank=True,null=True)
    # image_banner = models.ImageField(max_length=255,upload_to=image_to_url,blank=True,null=True)
    # image_prizes = models.ImageField(max_length=255,upload_to=image_to_url,blank=True,null=True)
    image_prizes = ResizedImageField(upload_to=upload_to1)
    image_first = ResizedImageField(upload_to=upload_to2)
    image_second = ResizedImageField(upload_to=upload_to3)
    image_third = ResizedImageField(upload_to=upload_to4)
    image_banner = ResizedImageField(upload_to=upload_to5, null=True, blank=True)

    # prizeImage=ResizedImageField(upload_to=upload_to1)
    # coverImage=ResizedImageField(upload_to=upload_to5,null=True,blank=True)
    # firstPrize=ResizedImageField(upload_to=upload_to2)
    # secondPrize=ResizedImageField(upload_to=upload_to3)
    # thirdPrize=ResizedImageField(upload_to=upload_to4)
    # new props

    banner_color = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Regular', blank=True)
    ticket_id = models.IntegerField(null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.LotteryName


class LotteryTicket(models.Model,SerializedModel):
    userLuckyNumber = models.CharField(primary_key=True, max_length=50)
    userInput = models.CharField(max_length=6)
    lotteryId = models.UUIDField()
    userId = models.IntegerField()
    purchaseTime = models.DateTimeField(auto_now_add=True)
    # quantity = models.IntegerField()

    # def save(self, *args, **kwargs):
    #     if not self.userLuckyNumber:
    #         random_digits_start = ''.join(random.choices(string.digits, k=4))
    #         random_digits_end = ''.join(random.choices(string.digits, k=4))
    #         self.userLuckyNumber = f"{random_digits_start}{self.userInput}{random_digits_end}"
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket #{self.userLuckyNumber} for User #{self.userId}"


class Winner(models.Model,SerializedModel):
    winnerId = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    ticketId = models.CharField(max_length=50)
    userId = models.IntegerField()
    prizeType = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    lotteryId = models.UUIDField()

    def __str__(self):
        return f"Winner: {self.winnerId}, Ticket #{self.ticketId}, User #{self.userId}"
