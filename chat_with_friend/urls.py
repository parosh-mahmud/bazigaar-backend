from django.urls import path 
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path("GetChatList/",views.GetChatList.as_view(),name="GetChatList"),
    path("GetCommunityChatList/",views.GetCommunityChatList.as_view(),name="GetCommunityChatList"),
    path("CreateChatWithFriend/",views.CreateChatWithFriend.as_view(),name="CreateChatWithFriend"),
    path("GetChatWithFriend/<pk>/",views.GetChatWithFriend.as_view(),name="GetChatWithFriend"),
    path("reactOnMessage/",views.reactOnMessage,name="reactOnMessage"),
    path("chatMessageExistOrNot/",views.chatMessageExistOrNot,name="chatMessageExistOrNot"),
    path("getChatByQuery/",views.getChatByQuery,name="getChatByQuery"),
    
    path("GetChatMessageList/",views.GetChatMessageList.as_view(),name="GetChatMessageList"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
