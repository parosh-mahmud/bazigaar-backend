from django.shortcuts import render
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth import get_user_model, login
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from AdminPanel.serializers import *
from ticket_draw_app.models import Ticket
from .serializers import CreateTicketSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


class CreateTicket(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreateTicketSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "New ticket created", "type": "success"})


class AllTicketList(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Ticket.objects.all()
    serializer_class = CreateTicketSerializer


@api_view(['GET'])
@permission_classes([IsAdminUser])  # IsAdminUser
def SingleTicketView(request, pk):
    try:
        id = pk
    except:
        return Response({"type": "error", "msg": "Ticket id is not found in request"})

    if Ticket.objects.filter(id=id).exists():
        queryset = Ticket.objects.get(id=id)
        serializer_class = CreateTicketSerializer(queryset, many=False)
        return Response(serializer_class.data)
    else:
        return Response({"type": "error", "msg": "Ticket id is not valid in our system"})


class UpdateMobileAPIView(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = CreateTicketSerializer
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Updated successfully", "type": "success"})

        else:
            return Response({"type": "error", "msg": serializer.errors})


@api_view(['POST'])
@permission_classes([IsAdminUser])  # IsAdminUser
def Active_Ticket(request):
    try:
        id = request.data["id"]
        if id == '':
            return Response({"type": "error", "msg": "id not found."})
    except:
        return Response({"type": "error", "msg": "id not sent."})

    Ticket.objects.filter(id=id).update(active=True)
    return Response({"type": "success", "msg": "Ticket activated."})


@api_view(['POST'])
@permission_classes([IsAdminUser])  # IsAdminUser
def DeActive_Ticket(request):
    try:
        id = request.data["id"]
        if id == '':
            return Response({"type": "error", "msg": "id not found."})
    except:
        return Response({"type": "error", "msg": "id not sent."})

    Ticket.objects.filter(id=id).update(active=False)
    return Response({"type": "success", "msg": "Ticket Disabled."})
