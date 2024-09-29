from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,AllowAny

@api_view(['GET'])
@permission_classes([IsAdminUser])
def updateLeaderDailyBoard(request):
    user=request.user
    return Response({})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def updateLeaderWeeklyBoard(request):
    user=request.user
    return Response({})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def updateLeaderMonthlyBoard(request):
    user=request.user
    return Response({})


@api_view(['GET'])
@permission_classes([AllowAny])
def getLeaderDailyBoard(request):
    return Response({})

@api_view(['GET'])
@permission_classes([AllowAny])
def getLeaderWeeklyBoard(request):
    return Response({})

@api_view(['GET'])
@permission_classes([AllowAny])
def getLeaderMonthlyBoard(request):
    return Response({})