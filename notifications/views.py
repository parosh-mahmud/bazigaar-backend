from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models, serializers
from django.utils.timezone import datetime
from django.contrib.auth import  get_user_model
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.generics import ListAPIView

class RequestNotificationList(ListAPIView):
    serializer_class = serializers.RequestNotificationSerializer
    def get_queryset(self):
        query_set=models.RequestNotification.objects.filter(
            Q(notification_to= self.request.user.id)
            ).order_by('-created_at')
        return query_set
class PromotionNotificationList(ListAPIView):
    serializer_class = serializers.PromotionNotificationSerializer
    def get_queryset(self):
        query_set=models.PromotionNotification.objects.filter(
            Q(notification_to= self.request.user.id) | Q(to_all=True)
            ).order_by('-created_at')
        return query_set
class GameNotificationList(ListAPIView):
    serializer_class = serializers.GameNotificationSerializer
    def get_queryset(self):
        query_set=models.GameNotification.objects.filter(
            Q(notification_to= self.request.user.id) | Q(to_all=True)
            ).order_by('-created_at')
        return query_set
class EventNotificationList(ListAPIView):
    serializer_class = serializers.EventNotificationSerializer
    def get_queryset(self):
        query_set=models.EventNotification.objects.filter(
            Q(notification_to= self.request.user.id) | Q(to_all=True)
            ).order_by('-created_at')
        return query_set