from django.urls import path 
from . import views

urlpatterns=[
    path("createAGroupCall/",views.createAGroupCall,name="createAGroupCall"),
    path("acceptGroupCall/",views.acceptGroupCall,name="acceptGroupCall"),
    path("raisedGroupCall/",views.raisedGroupCall,name="raisedGroupCall"),
    path("deniedGroupCall/",views.deniedGroupCall,name="deniedGroupCall"),
    path("endedGroupCall/",views.endedGroupCall,name="endedGroupCall"),
]