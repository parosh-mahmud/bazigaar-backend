import datetime
import random

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template, render_to_string
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.decorators import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


from .models import *
from .serializers import SliderSerializers, ViewSliderSerializer

# Create your views here.


class AddNewSlider(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = SliderSerializers

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"msg": "New Slider Added", "type": "success"})


class SliderListView(APIView):
    queryset = SliderModel.objects.filter().all()
    serializer_class = ViewSliderSerializer(queryset, many=True)
    permission_classes = [AllowAny,]

    def get(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = SliderModel.objects.filter().all()
        serializer_class = ViewSliderSerializer(queryset, many=True)
        j = 0
        arr = []
        for i in serializer_class.data:
            j = j+1
            i["id2"] = j
            if (i["active"] == "True"):
                i["active"] = True
            else:
                i["active"] = False
            arr.append(i)

        return Response(arr)


class SliderDetailsView(APIView):
    queryset = SliderModel.objects.filter().all()
    serializer_class = ViewSliderSerializer(queryset, many=True)
    permission_classes = [AllowAny, ]

    def get(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        s_id = request.query_params.get('id', None)
        queryset = SliderModel.objects.filter(id=s_id).all()
        serializer_class = ViewSliderSerializer(queryset, many=True)
        j = 0
        arr = []
        count = 1
        res = []
        for i in serializer_class.data:
            j = j + 1
            i["id2"] = j
            if (i["active"] == "True"):
                i["active"] = True
            else:
                i["active"] = False
            if count == id:
                return Response(i)
            arr.append(i)
            count += 1

        return Response(arr[0])


class SliderListViewByAdmin(APIView):
    permission_classes = [IsAdminUser,]
    queryset = SliderModel.objects.filter().all()
    serializer_class = ViewSliderSerializer(queryset, many=True)

    def get(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = SliderModel.objects.filter().all()
        serializer_class = ViewSliderSerializer(queryset, many=True)
        j = 0
        arr = []
        for i in serializer_class.data:
            j = j+1
            i["id2"] = j
            arr.append(i)

        return Response(arr)


class UpdateSliderAPIView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser,]
    queryset = SliderModel.objects.all()
    serializer_class = SliderSerializers
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"type": "success", "msg": "Slider updated successfully"})

        else:
            return Response({"type": "error", "msg": serializer.errors})


@api_view(['POST', 'PUT', 'PATCH'])
@permission_classes([AllowAny])
def ActiveSlider(request, pk):
    try:
        sliderID = pk
    except:
        return Response({"type": "error", "msg": "Slider not found"})

    if SliderModel.objects.filter(id=pk).exists():
        SliderModel.objects.filter(id=pk).update(active=True)
        return Response({"type": "success", "msg": "Slider active successfully"})
    else:
        return Response({"type": "error", "msg": "System failed to active this Slider"})

    return Response({"type": "error", "msg": "System failed. Try again"})


@api_view(['POST', 'PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def DeActiveSlider(request, pk):
    try:
        sliderID = pk
    except:
        return Response({"type": "error", "msg": "Slider not found"})

    if SliderModel.objects.filter(id=pk).exists():
        SliderModel.objects.filter(id=pk).update(active=False)
        return Response({"type": "success", "msg": "Slider De-active successfully"})
    else:
        return Response({"type": "error", "msg": "System failed to De-active this Slider"})

    return Response({"type": "error", "msg": "System failed. Try again"})


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_slider(request, pk):
    try:
        slider = SliderModel.objects.get(pk=pk)
    except SliderModel.DoesNotExist:
        return Response({"message": "Slider not found"}, status=404)

    slider.delete()
    return Response({"message": "Slider deleted successfully"}, status=204)
