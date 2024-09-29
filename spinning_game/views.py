from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .models import SpinningBatch,Bid
from .serializers import SpinningBatchSerializers,BidSerializers
from django.db.models import Q
from django.contrib.auth import  get_user_model
from rest_framework.permissions import AllowAny
from decimal import Decimal
import random

@api_view(["GET"])
@permission_classes([AllowAny])
def getOrCreateAndGetSpinning(request):
    utc_time = timezone.now()
    batchTime=utc_time.replace(second=0, microsecond=0)
    any=SpinningBatch.objects.filter(batchTime=batchTime)
    if any.exists():
        batch=any[0]
        return Response(SpinningBatchSerializers(batch).data)
    else:
        batch=SpinningBatch()
        batch.batchTime=batchTime
        batch.save()
        return Response(SpinningBatchSerializers(batch).data)


@api_view(["POST"])
def bidInSpin(request):
    user:get_user_model()=request.user
    batch=SpinningBatch.objects.get(id=request.data["batchId"])
    bidType=request.data["bidType"]
    amount=request.data["amount"]
    any=Bid.objects.filter(
        Q(batch=batch) &
        Q(bidType=bidType) &
        Q(bidder=user) 
    )
    if any.exists():
        user.bgcoin =user.bgcoin -Decimal(amount)
        user.save()
        bid:Bid=any[0]
        bid.batch=batch
        bid.bidder=user
        bid.amount=int(amount)+bid.amount
        bid.save()
        return Response(BidSerializers(bid).data)
    else:
        user.bgcoin =user.bgcoin - Decimal(amount)
        user.save()
        bid=Bid()
        bid.batch=batch
        bid.bidder=user
        bid.amount=int(amount)
        bid.bidType=bidType
        bid.save()
        return Response(BidSerializers(bid).data)


@api_view(["POST"])
def getWinner(request):
    batch=SpinningBatch.objects.get(id=request.data["batchId"])
    if batch.winField==None:
        bids=Bid.objects.filter(batch=batch)
        bids4x=bids.filter(bidType="4x")
        bids2x=bids.filter(bidType="2x")
        bids6x=bids.filter(bidType="6x")
        amountOf4x=0
        amountOf2x=0
        amountOf6x=0
        for each in bids4x :
            amountOf4x+=each.amount*4
        for each in bids2x :
            amountOf2x+=each.amount*2
        for each in bids6x :
            amountOf6x+=each.amount*6
        if amountOf2x<amountOf4x and amountOf2x<amountOf6x:
            batch.winField="2x"
            batch.winAmount=amountOf2x
            bids2x.update(win=True)
        elif amountOf4x<amountOf2x and amountOf4x<amountOf6x:
            batch.winField="4x"
            batch.winAmount=amountOf4x
            bids4x.update(win=True)
        elif amountOf6x<amountOf4x and amountOf6x<amountOf2x:
            batch.winField="6x"
            batch.winAmount=amountOf6x
            bids6x.update(win=True)
        elif amountOf6x==amountOf4x and amountOf6x==amountOf2x:
            batch.winField=random.choice(["2x","4x","6x"])
            batch.winAmount=amountOf2x
            bids2x.update(win=True)
                
        else:
            batch.winField="2x"
            batch.winAmount=amountOf2x
            bids2x.update(win=True)
        batch.save()
        return Response(SpinningBatchSerializers(batch).data)
    else:
        return Response(SpinningBatchSerializers(batch).data)

@api_view(["POST"])
def addWinningCoin(request):
    user=request.user
    batch=SpinningBatch.objects.get(id=request.data["batchId"])
    winField=batch.winField
    any=Bid.objects.filter(
        Q(bidder=user) &
        Q(batch=batch) &
        Q(bidType=winField) &
        Q(win=True)
    )
    if any.exists():
        bid=any[0]
        multiply=2
        if bid.bidType=="2x":
            multiply=2
        elif bid.bidType=="4x":
            multiply=4
        else:
            multiply=6
        winAmount=bid.amount*multiply
        user.bgcoin =user.bgcoin+winAmount
        user.save()
        return Response({"winAmount":winAmount})
    else:
        return Response({"winAmount":0})