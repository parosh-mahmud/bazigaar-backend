from django.contrib import admin
from .models import Ticket


@admin.action(description="Draw First Prize of Selected Ticket")
def drawFirstPrize(modeladmin, request, queryset):
    for ticket in queryset:
        pass


@admin.action(description="Draw Second Prize of Selected Ticket")
def drawSecondPrize(modeladmin, request, queryset):
    for ticket in queryset:
        pass


@admin.action(description="Draw Third Prize of Selected Ticket")
def drawThirdPrize(modeladmin, request, queryset):
    for ticket in queryset:
        pass
