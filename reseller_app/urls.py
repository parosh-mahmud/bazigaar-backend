from django.urls import path 
from . import views
from .views import  coin_request, get_coin_requests, reject_coin_request, \
    accept_coin_request, current_reseller, get_all_resellers, get_topup_history, ResellerCoinReqCreateAPIView, \
    ResellerCoinReqListAPIView, accept_status_by_doc_url, reject_status_by_doc_url, \
    get_requests_by_doc_url, create_reseller_coin_request

urlpatterns=[
    # path("reseller-login/", views.ResellerLoginView.as_view(),name="ResellerLoginView"),
    path("ResellerList/",views.resellers_list,name="ResellerList"),
    path("CreateTopUpRequest/",views.CreateTopUpRequest.as_view(),name="CreateTopUpRequest"),
    path("TopUpRequestList/",views.TopUpRequestList.as_view(),name="TopUpRequestList"),
    path("TopUpRequest/<int:pk>/",views.TopUpRequestById.as_view(),name="TopUpRequest"),
    path("topUpRequestStatusUpdate/",views.topUpRequestStatusUpdate,name="topUpRequestStatusUpdate"),
    # path("create-reseller/",views.CreateReseller.as_view()),
    path("accept-topup-request/",views.acceptTopupRequest),
    path("cancel-topup-request/",views.cancelTopupRequest),


    # path("res-signup/", signup),
    # path("res-login/", ResellerLoginView.as_view(),name="reseller-login"),
    path("res-coin-req/", coin_request),
    path("res-coin-req-view/<str:status>/", get_coin_requests),
    path("res-coin-req-reject/<int:request_id>/", reject_coin_request),
    path("res-coin-req-accept/<int:request_id>/<int:reseller_id>/", accept_coin_request),
    path("res-get-current/", current_reseller),
    path("res-get-all/", get_all_resellers,name='reseller-list'),
    ##
    path("get-topup-history/",get_topup_history),




    #reseller coin
    #make request
    path("request-coin-to-admin/",create_reseller_coin_request, name='request-coin-to-admin'),
    path("reseller-coin-req-list/", ResellerCoinReqListAPIView.as_view(), name='reseller-coin-req-list'),
    path("reseller-coin-req/", ResellerCoinReqCreateAPIView.as_view(), name='reseller-coin-req-list'),
    path('acc_status/', accept_status_by_doc_url, name='update_status'),
    path('rej_status/', reject_status_by_doc_url, name='update_status'),
    path('get_res_req_details/', get_requests_by_doc_url, name='get_reseller_req'),

]