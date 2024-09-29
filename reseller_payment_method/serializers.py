from rest_framework import serializers
from . import models

# show part


class SerializerCryptoCurrency(serializers.ModelSerializer):
    class Meta:
        model=models.CryptoCurrency
        fields="__all__"

class SerializerBankTransfer(serializers.ModelSerializer):
    class Meta:
        model=models.BankTransfer
        fields="__all__"

class SerializerMobileBanking(serializers.ModelSerializer):
    class Meta:
        model=models.MobileBanking
        fields="__all__"


# Request part

class SerializerPaymentRequestInBankTransfer(serializers.ModelSerializer):
    class Meta:
        model=models.PaymentRequestInBankTransfer
        fields="__all__"

class SerializerPaymentRequestInCryptoCurrency(serializers.ModelSerializer):
    class Meta:
        model=models.PaymentRequestInCryptoCurrency
        fields="__all__"

class SerializerPaymentRequestInMobileBanking(serializers.ModelSerializer):
    class Meta:
        model=models.PaymentRequestInMobileBanking
        fields="__all__"
