from django.urls import path 
from . import views

urlpatterns=[
    path("RequestNotificationList/",views.RequestNotificationList.as_view(),name="RequestNotificationList"),
    path("PromotionNotificationList/",views.PromotionNotificationList.as_view(),name="PromotionNotificationList"),
    path("GameNotificationList/",views.GameNotificationList.as_view(),name="GameNotificationList"),
    path("EventNotificationList/",views.EventNotificationList.as_view(),name="EventNotificationList"),
]