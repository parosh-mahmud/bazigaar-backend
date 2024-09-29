
from rest_framework import serializers
from . import models
from user_app.miniserializers import UserSerializerMini

class MobileBankModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.MobileBank
        fields="__all__"

class CryptoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Crypto
        fields="__all__"

class BankAccountModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.BankAccount
        fields="__all__"

class WalletDetailsModelSerializer(serializers.ModelSerializer):
    user=serializers.SerializerMethodField("getUser")
    mobileBanks=serializers.SerializerMethodField("getMobileBanks")
    cryptoBanks=serializers.SerializerMethodField("getCryptoBanks")
    bigBanks=serializers.SerializerMethodField("getBigBanks")
    class Meta:
        model=models.Wallet
        fields="__all__"
    def getUser(self,model):
        return UserSerializerMini(model.user,many=False).data
    def getMobileBanks(self,model):
        qs=models.MobileBank.objects.filter(wallet=model)
        return MobileBankModelSerializer(qs,many=True).data
    def getCryptoBanks(self,model):
        qs=models.Crypto.objects.filter(wallet=model)
        return CryptoModelSerializer(qs,many=True).data
    def getBigBanks(self,model):
        qs=models.BankAccount.objects.filter(wallet=model)
        return BankAccountModelSerializer(qs,many=True).data


class WalletSaveModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Wallet
        exclude=["user",]

class WithdrawalRequestSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.WithdrawalRequest
        fields="__all__"

    
class WithdrawalRequestDetailsModelSerializer(serializers.ModelSerializer):
    requestTo=serializers.SerializerMethodField("getRequest")
    user=serializers.SerializerMethodField("getUser")

    class Meta:
        model=models.WithdrawalRequest
        fields="__all__"
    def getUser(self,model):
        return UserSerializerMini(model.user,many=False).data
    def getRequest(self,model):
        requestTo=None
        mobile_bank=models.MobileBankWithdrawalRequet.objects.filter(withdrawalRequest__id=model.id)
        if len(mobile_bank)>0:
            requestTo=mobile_bank[0]
        bank=models.BankWithdrawalRequet.objects.filter(withdrawalRequest__id=model.id)
        if len(bank)>0:
            requestTo=bank[0]
        crypto=models.CryptoWithdrawalRequet.objects.filter(withdrawalRequest__id=model.id)
        if len(crypto)>0:
            requestTo=crypto[0]
    
        if requestTo!=None:
            return requestTo.data()
        else:
            return []

