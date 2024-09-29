from django.urls import path 
from . import views

urlpatterns=[
    path("GetCryptoCurrency/",views.GetCryptoCurrency.as_view(),name="GetCryptoCurrency"),
    path("GetBankTransfer/",views.GetBankTransfer.as_view(),name="GetBankTransfer"),
    path("GetMobileBanking/",views.GetMobileBanking.as_view(),name="GetMobileBanking"),
    path("CreateRequestOnBankPayment/",views.CreateRequestOnBankPayment.as_view(),name="CreateRequestOnBankPayment"),
    path("CreateRequestOnCryptoPayment/",views.CreateRequestOnCryptoPayment.as_view(),name="CreateRequestOnCryptoPayment"),
    path("CreateRequestOnMobilePayment/",views.CreateRequestOnMobilePayment.as_view(),name="CreateRequestOnMobilePayment"),
]