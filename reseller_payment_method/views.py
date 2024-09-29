from django.shortcuts import render

from . import serializers
from rest_framework import generics
from . import models


class CreateRequestOnCryptoPayment(generics.CreateAPIView):
    queryset = models.PaymentRequestInCryptoCurrency.objects.all()
    serializer_class = serializers.SerializerPaymentRequestInCryptoCurrency
class CreateRequestOnBankPayment(generics.CreateAPIView):
    queryset = models.PaymentRequestInBankTransfer
    serializer_class = serializers.SerializerPaymentRequestInBankTransfer
class CreateRequestOnMobilePayment(generics.CreateAPIView):
    queryset = models.PaymentRequestInMobileBanking
    serializer_class = serializers.SerializerPaymentRequestInMobileBanking



class GetCryptoCurrency(generics.ListAPIView):
    queryset = models.CryptoCurrency.objects.all()
    serializer_class = serializers.SerializerCryptoCurrency
class GetBankTransfer(generics.ListAPIView):
    queryset = models.BankTransfer.objects.all()
    serializer_class = serializers.SerializerBankTransfer
class GetMobileBanking(generics.ListAPIView):
    queryset = models.MobileBanking.objects.all()
    serializer_class = serializers.SerializerBankTransfer
    