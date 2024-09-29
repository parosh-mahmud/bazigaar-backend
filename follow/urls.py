from django.urls import path 
from . import views

urlpatterns=[
    path("follow_to/",views.follow_to,name="follow_to"),
    path("unfollow_to/",views.unfollow_to,name="unfollow_to"),
]