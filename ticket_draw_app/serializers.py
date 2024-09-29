from rest_framework import serializers
from . import models
from user_app.miniserializers import UserSerializerMini
from django.db.models import Q



class TicketSerializer(serializers.ModelSerializer):
    numberOfTicketSold=serializers.SerializerMethodField("getNumberOfTicketSold")
    winningRatio=serializers.SerializerMethodField("get_winningRatio")
    class Meta:
        model=models.Ticket
        fields="__all__"
    def getNumberOfTicketSold(self,model):
        queryset=models.LuckyNumber.objects.filter(
            Q(ticket=model)
        )
        return queryset.count()
    def get_winningRatio(self,model:models.Ticket):
        
        return f"{((model.numberOfWinner/model.totalNumberOfTickets)*100)} %" 



class LuckyNumberSerializer(serializers.ModelSerializer):
    buyer=serializers.SerializerMethodField("get_buyer")
    ticket=serializers.SerializerMethodField("get_ticket")
    class Meta:
        model=models.LuckyNumber
        fields="__all__"
    def get_buyer(self,model):
        return UserSerializerMini(model.buyer ,many=False).data
    def get_ticket(self,model):
        return TicketSerializer(model.ticket ,many=False).data


class LuckyNumberSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.LuckyNumber
        fields="__all__"


class TicketSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Ticket
        fields="__all__"

class TicketBuyHistorySerializer(serializers.ModelSerializer):
    buyer=serializers.SerializerMethodField("getBuyer")
    ticket=serializers.SerializerMethodField("getTicket")
    class Meta:
        model=models.TicketBuyHistory
        fields="__all__"
    def getBuyer(self,model:models.TicketBuyHistory):
        return UserSerializerMini(model.buyer ,many=False).data
    def getTicket(self,model:models.TicketBuyHistory):
        return TicketSerializer(model.ticket,many=False).data

class TicketWinnerSerializer(serializers.ModelSerializer):
    ticket=serializers.SerializerMethodField("get_ticket")
    luckyNumber=serializers.SerializerMethodField("get_luckyNumber")
    class Meta:
        model=models.TicketWinner
        fields="__all__"
    def get_ticket(self,model):
        return model.ticket.type
    def get_luckyNumber(self,model):
        return LuckyNumberSerializer(model.luckyNumber).data