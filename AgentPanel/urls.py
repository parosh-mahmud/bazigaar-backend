from django.urls import path 
from .views import AgentLoginView
from configurations.views import PageNotFound

urlpatterns=[
    path("agent-login/", AgentLoginView.as_view(),name="agent-login"),
    path("*", PageNotFound,name="404_page"),
]