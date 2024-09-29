from django.db import models
from base.base import SerializedModel
# Create your models here.
class FAQ(models.Model,SerializedModel):
    question=models.CharField(max_length=255)
    answer=models.TextField(max_length=5000)
    topic=models.CharField(max_length=127)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)