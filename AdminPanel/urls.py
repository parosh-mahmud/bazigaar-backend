from django.urls import path 
from .views import *
from configurations.views import PageNotFound

urlpatterns=[
    path("admin-login/", AdminLoginView.as_view(),name="admin-login"),
    path('hello/', AdminLoginView.as_view(), {'get': 'get_hello_world'}, name='hello-world'),
    # path("users-all/", AllUserData,name="users-all"),
    # path("agents-all/", AllAgentsData,name="agents-all"),
    # path("dashboard-info/", DashboardInfo,name="dashboard-info"),
    
    path("*", PageNotFound,name="page_not_found"),
]