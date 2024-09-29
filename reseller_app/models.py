import uuid

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth import get_user_model
from user_app.models import User
from notifications.models import RequestNotification
from base.base import SerializedModel


def awsKey(instance,filename,original_id):
    return "on test"

def upload_to(instance, filename):
    return 'image/screenshot/{filename}'.format(filename=filename)
def upload_to_reseller(instance, filename):
    return 'image/reseller_screenshot/{filename}'.format(filename=filename)

# generateResellerID
# def reseller_id_generate():
#     start_id = 100000
#     try:
#         current_id = Reseller().objects.filter().last()
#         reseller_user_id = start_id+current_id.id
#         return reseller_user_id
#     except:
#         return start_id
    
# class Reseller(AbstractUser):
#     user=models.ForeignKey(get_user_model(),on_delete=models.PROTECT,)
#     resellerId = models.UUIDField(default=uuid.uuid4(), editable=False, unique=True)
#     active = models.BooleanField(default=False)
#     amount = models.FloatField(default=0,null=True)
#     # whatsappNumber=models.CharField(max_length=20,blank=True,null=True)

#     groups = models.ManyToManyField(Group, related_name='reseller_users',null=True)
#     user_permissions = models.ManyToManyField(Permission, related_name='reseller_users',null=True)
#     created_at=models.DateTimeField(auto_now_add=True)
#     update_at=models.DateTimeField(auto_now=True)
    
#     def __str__(self) :
#         return self.resellerId





class CoinReq(models.Model,SerializedModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    request_id = models.AutoField(primary_key=True)
    reseller = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='coin_requests'
    )
    amount_req = models.FloatField()

    transaction_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"CoinReq by {self.reseller.email} - Status: {self.status}"

class ResellerHistory(models.Model,SerializedModel):
    resellerUserId=models.ForeignKey(get_user_model(),on_delete=models.PROTECT,related_name='ResellerModelID')
    createdBy=models.ForeignKey(get_user_model(),on_delete=models.PROTECT,related_name='ResellerCreatedAdminId')
    active = models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return str(self.id)
class TopUpRequest(models.Model,SerializedModel):
    reseller = models.ForeignKey(get_user_model(),on_delete=models.PROTECT,related_name="top_up_request_resellers")
    requestFrom = models.ForeignKey(get_user_model(),on_delete=models.PROTECT)
    amount = models.DecimalField(default=0,max_digits=20, decimal_places=2,)
    equalBgCoin = models.DecimalField(default=0,max_digits=20, decimal_places=2,)
    transactionId = models.CharField(max_length=50)
    transactionMedium = models.CharField(max_length=50)
    screenshot=ResizedImageField(upload_to=upload_to,blank=True,null=True)
    STATUS_CHOICES=(
        ("denied","denied"),
        ("pending","pending"),
        ("accepted","accepted")
    )
    status = models.CharField(max_length=20,default="pending",choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) :
        return str(self.status)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if not RequestNotification.objects.filter(objectRefId=str(self.id)).exists():
            object=RequestNotification()
            object.notification_from=self.requestFrom
            object.notification_to=self.reseller
            object.notification_type="request_for_coins"
            object.objectRefId=str(self.id)
            object.extended_text=str(self.equalBgCoin)+" coins."
            object.save()
        # return self

class TopUpRequestHistory(models.Model,SerializedModel):
    TopUpRequest = models.ForeignKey(TopUpRequest,on_delete=models.PROTECT)
    STATUS_CHOICES=(
        ("denied","denied"),
        ("pending","pending"),
        ("accepted","accepted")
    )
    status=models.CharField(max_length=20,default="pending",choices=STATUS_CHOICES)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return str(self.status)






from django.db import models
import os
import requests
def doc_path(instance, filename):
    #Perform the API call to upload the image
    url = "http://schoolproject-env.eba-ah3mewj2.ap-southeast-1.elasticbeanstalk.com/api/file"
    files = {"file": instance.document.file}
    response = requests.post(url, files=files)
    ret = "null"

    if response.status_code == 200:
        api_response = response.json()
        image_key = api_response.get("key", None)

        if image_key:
            # Extract the filename from the image_key
            filename = os.path.basename(image_key)

            # Create the directory if it doesn't exist
            directory = "reseller/doc/"
            os.makedirs(directory, exist_ok=True)

            # Save the image locally using the extracted filename
            local_image_path = os.path.join(directory, filename)
            with open(local_image_path, "wb") as f:
                f.write(files["file"].read())

            # Set the image_url field to the image_key value
            instance.doc_url = image_key

    # If the API call fails or no key is returned, return a default path or handle the error as needed
    return ret
# class ResellerCoinReq(models.Model):
#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('accepted', 'Accepted'),
#         ('rejected', 'Rejected'),
#     )

#     resellerId = models.IntegerField()
#     reseller_image_url = models.URLField(blank=True, null=True)
#     reseller_name = models.CharField(max_length=255)
#     transaction_number = models.CharField(max_length=100)
#     amount = models.DecimalField(max_digits=20, decimal_places=2)
#     bgcoin = models.DecimalField(max_digits=20, decimal_places=2)
#     document = models.FileField(upload_to=doc_path , blank=False)
#     doc_url = models.CharField(max_length=255,blank=True,null=True)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES,blank=True)
#     date = models.DateTimeField(auto_now=True)


#     def __str__(self):
#         return f"ResellerCoinReq: {self.reseller_name}, Transaction: {self.transaction_number}"


class ResellerCoinRequest(models.Model,SerializedModel):
    # STATUS_CHOICES = (
    #     ('pending', 'Pending'),
    #     ('accepted', 'Accepted'),
    #     ('rejected', 'Rejected'),
    # )

    # Auto-generated primary key field
    id = models.AutoField(primary_key=True)

    resellerId = models.IntegerField()
    reseller_image_url = models.URLField(blank=True, null=True)
    reseller_name = models.CharField(max_length=255)
    transaction_number = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    bgcoin = models.DecimalField(max_digits=20, decimal_places=2)
    document = models.FileField(upload_to=upload_to_reseller, blank=False)
    doc_url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10,  blank=True,default="pending")
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ResellerCoinReq: {self.reseller_name}, Transaction: {self.transaction_number}"
