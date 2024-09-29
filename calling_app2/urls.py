from django.urls import path 
from . import views

urlpatterns=[
    path("startCall/",views.startCall,name="startCall"),
    path("rejectCall/",views.rejectCall,name="rejectCall"),
    path("acceptCall/",views.acceptCall,name="acceptCall"),
    path("endCall/",views.endCall,name="endCall"),
    path("raisedCall/",views.raisedCall,name="raisedCall"),
 #   path("createIceCandidate/",views.createIceCandidate,name="createIceCandidate"),
]