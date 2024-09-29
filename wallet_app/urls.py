from django.urls import path
from . import views

urlpatterns = [
     # path('create-wallet/',views. create_wallet, name="rest_password_reset_confirm"),
    path('my-wallet/',views.WalletRetrieveUpdateDestroyAPIView.as_view(), name="wallet"),
    path('my-mobile-bank/',views.MobileBankRetrieveUpdateDestroyAPIView.as_view(),),
    path('my-crypto-bank/',views.CryptoRetrieveUpdateDestroyAPIView.as_view(),),
    path('my-big-bank/',views.BankAccountRetrieveUpdateDestroyAPIView.as_view(), ),
    path('withdrawal-req/',views.WithDrawRequestAPIView.as_view(), ),
    
    # admin
    path('wallet-list/<pk>/',views.WalletRetrieveUpdateDestroyAdminAPIView.as_view(), name="wallet"),
    path('wallet-list/',views.WalletListAdminAPIView.as_view(),),
    
    path('withdrawal-req/<pk>/',views.WithDrawRequestUpdateAPIView.as_view(),),
    path('withdrawal-req-list/',views.WithDrawRequestListAPIView.as_view(), ),
    
    path('withdrawal-req-list/<type>/',views.WithDrawRequestListFilterAPIView.as_view(),),
    
    # path('withdrawal-bank-req-list/<pk>/',views.WithDrawRequestUpdateAPIView.as_view(),),
    # path('withdrawal-bank-req-list/<pk>/',views.WithDrawRequestUpdateAPIView.as_view(),),
    
    # path('withdrawal-crypto-req-list/<pk>/',views.WithDrawRequestUpdateAPIView.as_view(),),
    # path('withdrawal-crypto-req-list/<pk>/',views.WithDrawRequestUpdateAPIView.as_view(),),

#get-wallet-number for mobile bank
    path('wallet-number/<pk>/',views.MobileBankRetrieveUpdateDestroyAdminAPIView.as_view(), ),
#get-wallet-bank for big bank
    path('wallet-bank/<pk>/',views.BankAccountRetrieveUpdateDestroyAdminAPIView.as_view(), ),
#get-wallet-crypto for crypto
    path('wallet-crypto/<pk>/',views.CryptoRetrieveUpdateDestroyAdminAPIView.as_view(), ),
    
    
    ]
