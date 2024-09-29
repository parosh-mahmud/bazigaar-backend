import json
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

# from Lottery.models import Lottery
# from Lottery.serializers import LotterySerializer
from . import serializers
# from . import views
from . import models
from rest_framework import response
# from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view, renderer_classes
from django.db.models import Q
# from chat_with_friend.models import ChatWithFriend
from user_app.models import User
from Lottery.models import LotteryTicket
import random
from decimal import Decimal
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
)

from .models import Ticket
from .serializers import TicketSerializer


class TicketListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Ticket.objects.filter(active=True).order_by("-created_at")
    serializer_class = TicketSerializer
    # permission_classes = [AllowAny,]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # print(serializer.data)
        return response.Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def ticket_list(request):
#     queryset = Ticket.objects.filter(active=True)

#     # Pagination logic
#     paginator = PageNumberPagination()
#     paginator.page_size = 10  # Adjust as needed
#     paginated_queryset = paginator.paginate_queryset(queryset, request)

#     serializer = TicketSerializer(paginated_queryset, many=True)

#     return paginator.get_paginated_response(serializer.data)


# class TicketBuyHistoryListAPIView(ListAPIView):
#     permission_classes = (IsAuthenticated)
#     queryset = models.TicketBuyHistory.objects.all()
#     serializer_class = serializers.TicketBuyHistorySerializer

#     def get_queryset(self):
#         return models.TicketBuyHistory.objects.filter()

#     def post(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def ticket_buy_history_list(request):
    user = request.user
    # print(user)
    if request.method == 'GET':
        # test = models.TicketBuyHistory.objects.filter(buyer=user)
        # testserializer = serializers.TicketBuyHistorySerializer(
        #     queryset, many=True)
        # print(testserializer.data)
        queryset = models.TicketBuyHistory.objects.filter(buyer=user)
        serializer = serializers.TicketBuyHistorySerializer(
            queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)

    elif request.method == 'POST':
        queryset = models.TicketBuyHistory.objects.filter(buyer=user)
        serializer = serializers.TicketBuyHistorySerializer(
            queryset, many=True)
        return Response(serializer.data)


# class LuckyNumberListAPIView(ListAPIView):
#     queryset = models.LuckyNumber.objects.all()
#     serializer_class = serializers.LuckyNumberSerializer

#     def get_queryset(self):
#         return models.LuckyNumber.objects.filter()

#     def post(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def lucky_number_list(request):
    id=request.GET.get("id",None)
    user = request.user
    if request.method == 'GET':
        queryset = models.LuckyNumber.objects.filter(buyer=user).filter(ticket__id=id)
        serializer = serializers.LuckyNumberSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        queryset = models.LuckyNumber.objects.filter(buyer=user).filter(ticket__id=id)
        serializer = serializers.LuckyNumberSerializer(queryset, many=True)
        return Response(serializer.data)


class TicketAPIView(RetrieveAPIView):
    queryset = models.Ticket.objects.all()
    serializer_class = serializers.TicketSerializer


class jsonencode():
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)


def convert_ticket_buy_history(ticketBuyHistory_obj, luckynumber, buyerid, lotteryuuid):
    lottery_obj = LotteryTicket()
    lottery_obj.userLuckyNumber = luckynumber
    lottery_obj.userInput = ticketBuyHistory_obj.pickNumber
    lottery_obj.userId = buyerid
    lottery_obj.lotteryId = lotteryuuid
    lottery_obj.purchaseTime = ticketBuyHistory_obj.purchaseDate

    lottery_obj.save()
    # print(lottery_obj)

    # return 0


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def purchaseTicket(request):
    count = int(request.data["count"])
    # if count is str:
    #     count=int(count)
    """
    The COUNT REPRESENT the number of tickets he wants to buy
    type is the ticket type
    numbers is the first 8 code number
    """
    request.data["id"]
    numbers = request.data["numbers"]
    user: User = request.user

    balance = user.bgtoken+user.bonusbgtoken
    any = models.Ticket.objects.filter(id=request.data["id"])
    if (any.exists()):
        ticket = any[0]
        amount = ticket.price * count
        if (balance > amount):
            bgtokenToCoin = 0
            if (user.bgtoken > amount):
                user.bgtoken -= amount
                bgtokenToCoin = amount
            else:
                amount -= user.bgtoken
                bgtokenToCoin = user.bgtoken
                user.bgtoken = 0
                user.bonusbgtoken -= amount
            coinReward = (bgtokenToCoin/100)*9
            user.bgcoin += Decimal(coinReward,)
            user.save()
            ticketBuyHistory = models.TicketBuyHistory()
            ticketBuyHistory.ticket = ticket
            ticketBuyHistory.buyer = user
            ticketBuyHistory.quantity = count
            ticketBuyHistory.pickNumber = numbers
            ticketBuyHistory.save()
            luckyNumbers = []
            for i in range(count):
                generated = generatedNumber(ticket, numbers)
                luckyNumber = models.LuckyNumber()
                luckyNumber.number = generated
                luckyNumber.buyer = user
                luckyNumber.ticket = ticket
                luckyNumber.save()
                luckyNumbers.append(luckyNumber)
                convert_ticket_buy_history(
                    ticketBuyHistory, generated, ticketBuyHistory.buyer.id, ticket.lotteryuuid)
            return response.Response(serializers.LuckyNumberSerializer(luckyNumbers, many=True).data)
    return response.Response({})


def generatedNumber(ticket, numbers):
    a = str(random.Random().randint(10000000, 99999999))
    generated = numbers+a
    any = models.LuckyNumber.objects.filter(
        Q(ticket=ticket) & Q(number=generated)
    )
    if (any.exists()):
        return generatedNumber(ticket, numbers)
    return generated


# @api_view(["POST"])
# def drawTicketFirstPrize(request):
#     print(request.data)
#     ticket_id=request.data["ticket_id"]
#     user:get_user_model()=request.user
#     if user.is_superuser:
#         query=models.Ticket.objects.filter(id=ticket_id)
#         if query.exists():
#             ticket=query[0]
#             if not ticket.firstPrizeDrawIsComplete:
#                 #
#                 winners=[]
#                 for i in range(ticket.numberOfFirstWinner):
#                     luckyNumbers=models.LuckyNumber.objects.filter(Q(ticket=ticket) & Q(win=False))
#                     random_index = random.randint(0, len(luckyNumbers)-1)
#                     winnerNumber=luckyNumbers[random_index]
#                     winnerNumber.win=True
#                     winnerNumber.save()
#                     ticketWinner=models.TicketWinner()
#                     ticketWinner.ticket=ticket
#                     ticketWinner.luckyNumber=winnerNumber
#                     ticketWinner.position=i+1
#                     ticketWinner.save()
#                     winners.append(ticketWinner)
#                 ticket.firstPrizeDrawIsComplete=True
#                 ticket.save()
#                 serializer=serializers.TicketWinnerSerializer(winners,many=True)
#                 return response.Response(serializer.data)
#             return response.Response({"msg":"First prize draw for the ticket is completed"})
#         return response.Response({"msg":"Ticket not found"})
#     else:
#         return response.Response({"msg":"your are not admin"})

# @api_view(["POST"])
# def drawTicketSecondPrize(request):
#     ticket_id=request.data["ticket_id"]
#     user:get_user_model()=request.user
#     if user.is_superuser:
#         query=models.Ticket.objects.filter(id=ticket_id)
#         if query.exists():
#             ticket=query[0]
#             if not ticket.secondPrizeDrawIsComplete:
#                 winners=[]
#                 for i in range(ticket.numberOfSecondWinner):
#                     luckyNumbers=models.LuckyNumber.objects.filter(Q(ticket=ticket) & Q(win=False))
#                     random_index = random.randint(0, len(luckyNumbers)-1)
#                     winnerNumber=luckyNumbers[random_index]
#                     winnerNumber.win=True
#                     winnerNumber.save()
#                     ticketWinner=models.TicketWinner()
#                     ticketWinner.ticket=ticket
#                     ticketWinner.luckyNumber=winnerNumber
#                     ticketWinner.position=i+1 +ticket.numberOfFirstWinner
#                     ticketWinner.save()
#                     winners.append(ticketWinner)
#                 ticket.secondPrizeDrawIsComplete=True
#                 ticket.save()
#                 serializer=serializers.TicketWinnerSerializer(winners,many=True)
#                 return response.Response(serializer.data)
#             return response.Response({"msg":"First prize draw for the ticket is completed"})
#         return response.Response({"msg":"Ticket not found"})
#     else:
#         return response.Response({"msg":"your are not admin"})

# @api_view(["POST"])
# def drawTicketThirdPrize(request):
#     ticket_id=request.data["ticket_id"]
#     user:get_user_model()=request.user
#     if user.is_superuser:
#         query=models.Ticket.objects.filter(id=ticket_id)
#         if query.exists():
#             ticket=query[0]
#             if not ticket.thirdPrizeDrawIsComplete:
#                 #
#                 luckyNumbers=models.LuckyNumber.objects.filter(Q(ticket=ticket) & Q(win=False))
#                 winners=[]
#                 for i in range(ticket.numberOfThirdWinner):
#                     luckyNumbers=models.LuckyNumber.objects.filter(Q(ticket=ticket) & Q(win=False))
#                     random_index = random.randint(0, len(luckyNumbers)-1)
#                     winnerNumber=luckyNumbers[random_index]
#                     winnerNumber.win=True
#                     winnerNumber.save()
#                     ticketWinner=models.TicketWinner()
#                     ticketWinner.ticket=ticket
#                     ticketWinner.luckyNumber=winnerNumber
#                     ticketWinner.position=i+1+ticket.numberOfFirstWinner+ticket.numberOfSecondWinner
#                     ticketWinner.save()
#                     winners.append(ticketWinner)
#                 ticket.thirdPrizeDrawIsComplete=True
#                 ticket.save()
#                 serializer=serializers.TicketWinnerSerializer(winners,many=True)
#                 return response.Response(serializer.data)
#             return response.Response({"msg":"First prize draw for the ticket is completed"})
#         return response.Response({"msg":"Ticket not found"})
#     else:
#         return response.Response({"msg":"your are not admin"})
