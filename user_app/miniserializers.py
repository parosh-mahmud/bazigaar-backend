from . import models
from rest_framework import serializers
from follow.models import Follow
from django.db.models import Q
from django.utils.timezone import now
from base.base import imageToUrl


class UserSerializerMini(serializers.ModelSerializer):
    noOfFollowers = serializers.SerializerMethodField("getNoOfFollowers")
    isOnline = serializers.SerializerMethodField("getIsOnline")

    class Meta:
        model = models.User
        fields = ['profile_picture', 'nickname', 'id', 'first_name',
                  'last_name', 'noOfFollowers', 'isOnline', 'countryCode', 'email', 'country', 'address', 'city', 'state', 'postal_code', 'gender', 'phoneNumber', 'date_of_birth']

    # def validate_profile_picture(self, value):
    #     if isinstance(value, list):
    #         for item in value:
    #             if isinstance(item, str) and '/media' in item:
    #                 return None  # Return None to exclude profile_picture from update
    #     return value

    # def update(self, instance, validated_data):
    #     # Update each field in the instance
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance

    def getNoOfFollowers(self, model):
        return len(Follow.objects.filter(Q(follow_to=model) & Q(active=True)))

    def getIsOnline(self, model):
        return model.online
