from django.db import models
from django.contrib.auth import get_user_model
from base.base import SerializedModel

class ContactUsMessage(models.Model,SerializedModel):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    name=models.CharField(max_length=127)
    email=models.CharField(max_length=127)
    subject=models.CharField(max_length=127)
    message=models.CharField(max_length=2000)