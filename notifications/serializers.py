from rest_framework import serializers
from . import models
from user_app.miniserializers import UserSerializerMini

class RequestNotificationSerializer(serializers.ModelSerializer):
    notification_to=serializers.SerializerMethodField("get_notification_to")
    notification_from=serializers.SerializerMethodField("get_notification_from")
    class Meta:
        model=models.RequestNotification
        fields="__all__"
    def get_notification_to(self,model:models.RequestNotification):
        return UserSerializerMini(model.notification_to,many=False).data
    def get_notification_from(self,model:models.RequestNotification):
        return UserSerializerMini(model.notification_from,many=False).data


class RequestNotificationSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.RequestNotification
        fields="__all__"


class PromotionNotificationSerializer(serializers.ModelSerializer):
    notification_to=serializers.SerializerMethodField("get_notification_to")
    notification_from=serializers.SerializerMethodField("get_notification_from")
    class Meta:
        model=models.PromotionNotification
        fields="__all__"
    def get_notification_to(self,model:models.RequestNotification):
        if model.notification_to==None:
            return
        return UserSerializerMini(model.notification_to,many=False).data
    def get_notification_from(self,model:models.RequestNotification):
        if model.notification_from==None:
            return
        return UserSerializerMini(model.notification_from,many=False).data


class GameNotificationSerializer(serializers.ModelSerializer):
    notification_to=serializers.SerializerMethodField("get_notification_to")
    notification_from=serializers.SerializerMethodField("get_notification_from")
    class Meta:
        model=models.GameNotification
        fields="__all__"
    def get_notification_to(self,model:models.RequestNotification):
        if model.notification_to==None:
            return
        return UserSerializerMini(model.notification_to,many=False).data
    def get_notification_from(self,model:models.RequestNotification):
        if model.notification_from==None:
            return
        return UserSerializerMini(model.notification_from,many=False).data


class EventNotificationSerializer(serializers.ModelSerializer):
    notification_to=serializers.SerializerMethodField("get_notification_to")
    notification_from=serializers.SerializerMethodField("get_notification_from")
    class Meta:
        model=models.EventNotification
        fields="__all__"
    def get_notification_to(self,model:models.RequestNotification):
        if model.notification_to==None:
            return
        return UserSerializerMini(model.notification_to,many=False).data
    def get_notification_from(self,model:models.RequestNotification):
        if model.notification_from==None:
            return
        return UserSerializerMini(model.notification_from,many=False).data
