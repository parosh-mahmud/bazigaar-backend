from rest_framework import serializers
from .models import SpinningBatch,Bid

class SpinningBatchSerializers(serializers.ModelSerializer):
    class Meta:
        model=SpinningBatch
        fields="__all__"

class BidSerializers(serializers.ModelSerializer):
    class Meta:
        model=Bid
        fields="__all__"