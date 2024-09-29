from django.urls import path 
from . import views

urlpatterns=[
    path('getLiveStreams/',views.getLiveStreams,name="getLiveStreams"),
    path('getLiveStreamSSE/',views.getLiveStreamSSE,name="getLiveStreamSSE"),
    path('getSingleLiveStream/',views.getSingleLiveStream,name="getSingleLiveStream"),
    path('commentHere/',views.commentHere,name="commentHere"),
    path('createALiveStream/',views.createALiveStream,name="createALiveStream"),
    path('updateALiveStream/',views.updateALiveStream,name="updateALiveStream"),
]