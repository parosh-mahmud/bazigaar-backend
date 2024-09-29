from django.urls import path 
from . import views

urlpatterns=[
    path("CreateChatInGroup/",views.CreateChatInGroup.as_view(),name="CreateChatInGroup"),
    path("GetCommunityChats/",views.GetCommunityChats.as_view(),name="GetCommunityChats"),
    path("GetCommunityChat/<pk>/",views.GetCommunityChat.as_view(),name="GetCommunityChat"),
    path("CreateGroupMessage/",views.CreateGroupMessage.as_view(),name="CreateGroupMessage"),
    path("reactOnMessage/",views.reactOnMessage,name="reactOnMessage"),
]