from rest_framework import serializers
from . import models

class ContactUsMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ContactUsMessage
        fields="__all__"