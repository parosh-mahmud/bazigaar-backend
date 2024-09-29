from datetime import datetime, timedelta

from rest_framework import serializers
from .models import Lottery, Winner, LotteryTicket


class LotterySerializer(serializers.ModelSerializer):
    # ClosingTime = Lottery.ClosingTime
    remaining_time = serializers.SerializerMethodField()
    remaining_time_seconds = serializers.SerializerMethodField()
    tickets_sold = serializers.SerializerMethodField()

    class Meta:
        model = Lottery
        fields = '__all__'
        read_only_fields = ('LotteryId',)

    def get_remaining_time(self, obj):
        # Calculate the remaining time between the current time and the closing time
        remaining_time = obj.ClosingTime - datetime.now(obj.ClosingTime.tzinfo)
        # remaining_time = datetime.now()
        # remaining_time = datetime.now()
        remaining_seconds = max(remaining_time.total_seconds(), 0)
        return self.format_remaining_time(remaining_seconds)

    def get_remaining_time_seconds(self, obj):
        # Calculate the remaining time in seconds between the current time and the closing time
        remaining_time = obj.ClosingTime - datetime.now(obj.ClosingTime.tzinfo)
        # remaining_time = datetime.now()
        remaining_seconds = max(remaining_time.total_seconds(), 0)
        return int(remaining_seconds)

    @staticmethod
    def format_remaining_time(seconds):
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        remaining_time_str = ""
        if days > 0:
            remaining_time_str += f"{int(days)} days, "
        if hours > 0:
            remaining_time_str += f"{int(hours)} hours, "
        if minutes > 0:
            remaining_time_str += f"{int(minutes)} minutes, "
        remaining_time_str += f"{int(seconds)} seconds"

        return remaining_time_str
    def get_tickets_sold(self, obj):
        # Query the number of LotteryTicket objects with the same lottery_id
        return LotteryTicket.objects.filter(lotteryId=obj.LotteryId).count()

class LotteryTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = LotteryTicket
        fields = '__all__'
class WinnerTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Winner
        fields = '__all__'

