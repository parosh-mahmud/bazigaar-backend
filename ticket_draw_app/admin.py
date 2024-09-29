from django.contrib import admin
from . import models
# Register your models here.

admin.site.register([models.LuckyNumber,models.Ticket,models.TicketBuyHistory,models.TicketWinner])