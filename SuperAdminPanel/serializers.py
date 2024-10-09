from rest_framework import serializers
from ticket_draw_app.models import *
from user_app.models import *
from django.db.models import Q

class CreateTicketSerializer(serializers.ModelSerializer):
    # prizeImage = serializers.ImageField(required=False)
    # firstPrize = serializers.ImageField(required=False)
    # secondPrize = serializers.ImageField(required=False)
    # thirdPrize = serializers.ImageField(required=False)
    # coverImage = serializers.ImageField(required=False)
    prizeImage = serializers.CharField(required=False)
    firstPrize = serializers.CharField(required=False)
    secondPrize = serializers.CharField(required=False)
    thirdPrize = serializers.CharField(required=False)
    coverImage = serializers.CharField(required=False)
    print("--coverImage--", coverImage)
    class Meta:
        model=Ticket
        fields="__all__"
        expandable_fields = {
            'prizeImage': ('reviews.ImageSerializer', {'many': True}),
            'firstPrize': ('reviews.ImageSerializer', {'many': True}),
            'secondPrize': ('reviews.ImageSerializer', {'many': True}),
            'thirdPrize': ('reviews.ImageSerializer', {'many': True}),
            'coverImage': ('reviews.ImageSerializer', {'many': True}),
        }

class AdminUserUpdateSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)
    class Meta:
        model=User
        # fields="__all__"
        expandable_fields = {
            'profile_picture': ('reviews.ImageSerializer', {'many': True}),
        }
        exclude=['password','email']

