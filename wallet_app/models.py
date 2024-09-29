from django.db import models
import uuid
from user_app.models import User
from base.base import SerializedModel


class Wallet(models.Model,SerializedModel):
    wallet_id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user= models.OneToOneField(User, on_delete=models.CASCADE)


class MobileBank(models.Model,SerializedModel):
    wallet=models.ForeignKey(Wallet,on_delete=models.CASCADE)
    number= models.CharField(max_length=50)
    # TYPES=(
    #     ("BKASH","bkash"),
    #     ("NAGAD","nagad"),
    #     ("ROCKET","rocket")
    # )
    bankName = models.CharField(max_length=50)


class Crypto(models.Model,SerializedModel):
    address= models.CharField(max_length=100)
    networkName=models.CharField(max_length=50)
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    cryptoName = models.CharField(max_length=50)
    
class BankAccount(models.Model,SerializedModel):
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    accountNumber = models.CharField(max_length=250)
    accountHolderName=models.CharField(max_length=250)
    bankName=models.CharField(max_length=250)
    branchName = models.CharField(max_length=250)




class WithdrawalRequest(models.Model,SerializedModel):
    user=models.ForeignKey(User,on_delete=models.PROTECT,null=True)
    #MobileBank,Crypto,Bank etc
    type=models.CharField(max_length=55,)
    status=models.CharField(max_length=55,default="Pending")#Approved,Denied
    created_at=models.DateTimeField(auto_now_add=True)

class MobileBankWithdrawalRequet(models.Model,SerializedModel):
    withdrawalRequest=models.ForeignKey(WithdrawalRequest,on_delete=models.CASCADE)
    amount=models.CharField(max_length=10,)
    bankName=models.CharField(max_length=27,)
    number=models.CharField(max_length=27,)

class BankWithdrawalRequet(models.Model,SerializedModel):
    withdrawalRequest=models.ForeignKey(WithdrawalRequest,on_delete=models.CASCADE)
    amount=models.CharField(max_length=10,)
    accountNumber = models.CharField(max_length=250)
    accountHolderName=models.CharField(max_length=250)
    bankName=models.CharField(max_length=250)
    branchName = models.CharField(max_length=250)

class CryptoWithdrawalRequet(models.Model,SerializedModel):
    withdrawalRequest=models.ForeignKey(WithdrawalRequest,on_delete=models.CASCADE)
    amount=models.CharField(max_length=10,)
    address= models.CharField(max_length=100)
    networkName=models.CharField(max_length=50)
    cryptoName = models.CharField(max_length=50)
