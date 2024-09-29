from django.db import models
from django.contrib.auth import get_user_model
from base.base import SerializedModel


class Follow(models.Model,SerializedModel):
    user=models.ForeignKey(get_user_model(),on_delete=models.PROTECT,related_name="follow_to_s")
    follow_to=models.ForeignKey(get_user_model(),on_delete=models.PROTECT,related_name="followers")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    active=models.BooleanField(default=True)