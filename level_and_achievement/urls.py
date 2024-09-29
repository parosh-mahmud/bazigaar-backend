from django.urls import path 
from . import views

urlpatterns=[
    path("createUserLevel/",views.createUserLevel,name="createUserLevel"),
    path("getAllAchievements/",views.getAllAchievements,name="getAllAchievements"),
    path("getAllUserAchievements/",views.getAllUserAchievements,name="getAllUserAchievements"),
    path("claimPoints/",views.claimPoints,name="getAllUserAchievements")



]