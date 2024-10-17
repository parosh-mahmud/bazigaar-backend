import string
import random
import uuid
from django.db import models
from django.db.models import CASCADE
from django_resized import ResizedImageField
from django.utils.timezone import now,timedelta
from base.base import SerializedModel
from django.contrib.auth.models import AbstractUser


def upload_to(instance, filename):
    return 'image/profile/{filename}'.format(filename=filename)

def generate_random_string(length=6):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))
# {'nickname': ' onug', 'first_name': 'onirudda', 'last_name': 'islam', 'gender': 'M'}


class User(AbstractUser,SerializedModel):
    profile_picture=ResizedImageField( upload_to=upload_to,blank=True, null=True,)
    isHost=models.BooleanField(default=False)
    # isReseller=models.BooleanField(default=False)
    first_name=models.CharField(max_length=255,null=False,default="",blank=True)
    last_name=models.CharField(max_length=255,null=False,default="",blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_agent=models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_premium=models.BooleanField(default=False)
    nickname=models.CharField(max_length=255,null=False,default="",blank=True)
    GENDER_CHOICES =(
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
    )
    online=models.BooleanField(default=False)
    isReseller=models.BooleanField(default=False)
    gender=models.CharField(max_length=7,choices=GENDER_CHOICES)
    date_of_birth=models.DateField(null=True)
    last_online=models.DateTimeField(auto_now=True)
    countryCode=models.CharField(max_length=10,null=True,blank=True)
    phoneNumber=models.CharField(max_length=20,null=True,blank=True)
    
    bgcoin=models.DecimalField(default=0.0,max_digits=20,decimal_places=2) 
    bonusbgcoin=models.DecimalField(default=0.0,max_digits=20,decimal_places=2) #RM

    bgtoken=models.DecimalField(default=0.0,max_digits=20,decimal_places=2)
    bonusbgtoken=models.DecimalField(default=0.0,max_digits=20,decimal_places=2)

    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    device_name = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.CharField(max_length=100, null=True, blank=True)
    operating_system = models.CharField(max_length=100, null=True, blank=True)
    src = models.CharField(max_length=255, blank=True, null=True)
    ref = models.CharField(max_length=6, default=generate_random_string)
    #____________joined at___________
    def __str__(self) :
        print(self.email)
        print(self.id)
        print(self.nickname)
        print(self.username)
        return self.email +" "+str(self.id) +" "+self.nickname +" "+self.username



class ResetPasswordModel(models.Model,SerializedModel):
    key=models.CharField(max_length=10)
    email=models.EmailField()
    created_at=models.DateTimeField(auto_now_add=True)
    def isExpired(self):
        expire_time = now() - timedelta(minutes=2)
        return  self.created_at < expire_time

class Referral(models.Model,SerializedModel):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_by')
    date_referred = models.DateTimeField(auto_now_add=True)
    referrer_code = models.CharField(max_length=10, unique=True)

# class Wallet(models.Model):
#     wallet_id = models.UUIDField(primary_key=True,default=uuid.uuid4, auto_created=True)
#     user= models.ForeignKey(User, on_delete=CASCADE)
#     CRYPTO_CHOICES=(
#         ("ETH","eth"),
#         ("BTC","btc"),
#         ("NONE","none")
#     )
#     crypto = models.CharField(choices=CRYPTO_CHOICES, default="NONE",max_length=50)
#     crypto_id = models.CharField(max_length=255,blank=True,null=True)
# class WalletNumbers(models.Model):
#     wallet_number_id = models.UUIDField(primary_key=True, auto_created=True)
#     Number= models.CharField(max_length=50)
#     wallet = models.ForeignKey(Wallet,on_delete=CASCADE)
#     TYPES=(
#         ("BKASH","bkash"),
#         ("NAGAD","nagad"),
#         ("ROCKET","rocket")
#     )
#     number_type = models.CharField(choices=TYPES,max_length=50)
#     Image = models.CharField(max_length=250,null=True)
# class WalletCryptoNumbers(models.Model):
#     wallet_number_id = models.UUIDField(primary_key=True, auto_created=True)
#     CryptoWalletNumber= models.CharField(max_length=50)
#     NetworkName=models.CharField(max_length=50)
#     wallet = models.ForeignKey(Wallet,on_delete=CASCADE)
#     TYPES=(
#         ("BITCOIN","bitcoin"),
#         ("LEETCOIN","leetcoin"),
#         ("ETHERIUM","etherium")
#     )
#     number_type = models.CharField(choices=TYPES,max_length=50)
#     Image = models.CharField(max_length=250,null=True)

# class WalletBankAccounts(models.Model):
#     wallet_number_id = models.UUIDField(primary_key=True, auto_created=True)
#     wallet = models.ForeignKey(Wallet,on_delete=CASCADE)
#     TYPES=(
#         ("BRAC Bank Ltd","BRAC Bank Ltd"),
#         ("Islami Bank Ltd","Islami Bank Ltd"),
#         ("DBBL","DBBL"),
#         ("Pubali Bank Ltd", "Pubali Bank Ltd")
#     )
#     Account_Number = models.CharField(max_length=250)
#     Account_Holder_Name=models.CharField(max_length=250)
#     BankName=models.CharField(choices=TYPES,max_length=250)
#     BranchName = models.CharField(max_length=250)
#     Image = models.CharField(max_length=250,null=True)


