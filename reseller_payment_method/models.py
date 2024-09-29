from django.db import models
from base.base import SerializedModel


def upload_to(instance, filename):
    return 'attachment/{filename}'.format(filename=filename)


class CryptoCurrency(models.Model,SerializedModel):
    name=models.CharField(max_length=56)
    qrCodeImage=models.ImageField(null=True,blank=True,upload_to="QRCode/")
    network=models.CharField(max_length=56)
    depositAddress=models.CharField(max_length=128)
    

    def __str__(self) :
        return str(self.id)    

class BankTransfer(models.Model,SerializedModel):
    name=models.CharField(max_length=128)
    accountHolderName=models.CharField(max_length=128)
    accountNumber=models.CharField(max_length=128)
    branchName=models.CharField(max_length=56)

    def __str__(self) :
        return str(self.id)
class MobileBanking(models.Model,SerializedModel):
    name=models.CharField(max_length=56)
    number=models.CharField(max_length=20)
    def __str__(self) :
        return str(self.id)
class PaymentRequestInCryptoCurrency(models.Model,SerializedModel):
    cryptoCurrency=models.ForeignKey(CryptoCurrency,on_delete=models.CASCADE)
    attactment=models.ImageField(upload_to=upload_to,null=True)
    note=models.TextField(max_length=500,blank=True,default="",null=True)
    #accepted , denied
    ammountInDollar=models.CharField(max_length=30,null=True)
    ammountInBGCOIN=models.CharField(max_length=30,null=True)

    STATUS_OPTIONS=(
        ("PENDING","pending"),
        ("ACCEPTED","accepted"),
        ("CANCEL","cancel"),
    )
    status=models.CharField(default="pending",choices=STATUS_OPTIONS,max_length=20)

    def __str__(self) :
        return str(self.id)
class PaymentRequestInBankTransfer(models.Model,SerializedModel):
    bankTransfer=models.ForeignKey(BankTransfer,on_delete=models.CASCADE)
    attactment=models.ImageField(upload_to=upload_to,null=True)
    note=models.TextField(max_length=500,blank=True,default="",null=True)
    ammountInDollar=models.CharField(max_length=30,null=True)
    ammountInBGCOIN=models.CharField(max_length=30,null=True)
    STATUS_OPTIONS=(
        ("PENDING","pending"),
        ("ACCEPTED","accepted"),
        ("CANCEL","cancel"),
    )
    status=models.CharField(default="pending",choices=STATUS_OPTIONS,max_length=20)

    def __str__(self) :
        return str(self.id)
    
class PaymentRequestInMobileBanking(models.Model,SerializedModel):
    mobileBanking=models.ForeignKey(MobileBanking,on_delete=models.CASCADE)
    attactment=models.ImageField(upload_to=upload_to,null=True)
    note=models.TextField(max_length=500,blank=True,default="",null=True)
    ammountInDollar=models.CharField(max_length=30,null=True)
    ammountInBGCOIN=models.CharField(max_length=30,null=True)
    STATUS_OPTIONS=(
        ("PENDING","pending"),
        ("ACCEPTED","accepted"),
        ("CANCEL","cancel"),
    )

    status=models.CharField(default="pending",choices=STATUS_OPTIONS,max_length=20)
    def __str__(self) :
        return str(self.id)

