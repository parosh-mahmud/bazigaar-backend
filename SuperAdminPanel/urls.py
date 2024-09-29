from django.urls import path 
from .views import *
from configurations.views import PageNotFound
from .ticket import *

urlpatterns=[

    path("admin-login/", UserLoginView.as_view()),
    path("users-all/", AllUserData),
    path("all-general-users/", all_general_user),
    path("all-resellers/", all_resellers),
    path("users-active-all/", AllUserData),
    path("users-block-all/", all_blocked_user),
    path("users/<str:pk>/", SingleUserData),
    path('block-user/<int:user_id>/', BlockUserView, name='block-user'),
    path('add-bgcoin/<int:user_id>/', AddBGCoin, name='add-bgcoin'),
    path('sub-bgcoin/<int:user_id>/', SubBGCoin, name='add-bgcoin'),
    path('convert-coin-to-token/', convert_coin_to_token, name='convert-to-token'),

    path("agents-all/", AllAgentsData),
    path("agents/<str:pk>/", SingleAgentsData),
    path("reseller-all/", AllReseller),
    path("reseller/<str:pk>/", SingleReseller),
    path("email-unverified-all/", AllUnverifiedEmailUser),
    path('dashboard-info/',Test),
    path('dashboard-chart/',chart),
    path("user-update/<str:pk>/", userDataUpdate.as_view()),

    
    # make host active / deactive
    path("active-host/", Active_Host,name="active-host"),
    path("de-active-host/", DeActive_Host,name="de-active-host"),
    
    # ticket

    path("create-new-ticket/", CreateTicket.as_view()),
    path("ticket/<str:pk>/", SingleTicketView),
    
    path("update-ticket/<str:pk>/", UpdateMobileAPIView.as_view(),name="UpdateMobileAPIView"),
    path("active-ticket/", Active_Ticket,name="Active_Ticket"),
    path("de-active-ticket/", DeActive_Ticket,name="DeActive_Ticket"),
    
    
    #host
    path("host-all/", AllHostList),
    path("host/<str:pk>/", SingleHostList),
    
    path("*", PageNotFound,name="page_not_found"),
]