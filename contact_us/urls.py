from django.urls import path 
from . import views

urlpatterns=[
    path("CreateContactUsMessage/",views.CreateContactUsMessage.as_view(),name="CreateContactUsMessage")
]