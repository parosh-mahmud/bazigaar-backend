from django.urls import path
from . import views

urlpatterns=[
   path('',views.notification_stream,name="sse"),
]