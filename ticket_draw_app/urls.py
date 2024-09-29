from django.urls import path
from . import views

urlpatterns = [
    path("ticketList/", views.TicketListAPIView.as_view(), name="ticketList"),

    # path("ticketList/", views.ticket_list, name="ticketList"),
    path("ticket/<pk>/", views.TicketListAPIView.as_view(), name="ticket"),
    path("purchaseTicket/", views.purchaseTicket, name="purchaseTicket"),
    # path("ticketBuyHistories/",views.TicketBuyHistoryListAPIView.as_view(),name="ticketBuyHistories"),
    path("ticketBuyHistories/", views.ticket_buy_history_list,
         name="ticketBuyHistories"),
    # path("luckynumberlist/", views.LuckyNumberListAPIView.as_view(),
    #      name="luckynumberlist"),
    path("luckynumberlist/", views.lucky_number_list,
         name="luckynumberlist"),
    # path("drawTicketFirstPrize/",views.drawTicketFirstPrize,name="drawTicketFirstPrize"),
    # path("drawTicketSecondPrize/",views.drawTicketSecondPrize,name="drawTicketSecondPrize"),
    # path("drawTicketThirdPrize/",views.drawTicketThirdPrize,name="drawTicketThirdPrize"),
]
