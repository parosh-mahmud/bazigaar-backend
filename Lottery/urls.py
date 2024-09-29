from django.urls import path, include 
from .views import *
from configurations.views import PageNotFound
from dj_rest_auth.views import LogoutView


urlpatterns=[
    path("test/", Test),
    # path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path("user-login/",UserLoginView.as_view(), name="admin-login"),
    path("make-reseller/", make_reseller, name="make-reseller"),
    path('get-all/', lottery_list, name='lottery-list'),
    path('get-all/open/', open_lottery_list, name='open-lottery-list'),
    path('get-all/closed/', closed_lottery_list, name='closed-lottery-list'),
    path('create/', create_lottery, name='lottery-creation'),
    path('create-with-file/', create_lottery_form, name='lottery-creation-test'),
    path('details/', get_lottery, name='get-lottery'),
    path('edit/', edit_lottery, name='edit-lottery'),
    path('delete/', delete_lottery, name='delete-lottery'),

    #tickets
    path('all-tickets/', all_tickets_in_lottery, name='all-tickets'),
    ## lottery purchase
    # path('user-purchase-lottery-ticket/', user_purchase_lottery_ticket, name='purchase-ticket'),
    path('user-tickets-in-lottery/', user_tickets_in_lottery, name='user-tickets'),

    # open lottery list
    # close a lottery
    # open a lottery
    # lottery draw
    path('draw-lottery/', draw_ticket, name='draw-ticket'),
    path('draw-lottery-winners/', winner_list, name='draw-ticket'),
    # check if a lottery is open before purchase
    path("*", PageNotFound, name="page_not_found")

]