from rest_framework.decorators import api_view, permission_classes
from . import models
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
import uuid
from django.http import Http404
from . import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from decimal import Decimal
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
# from django.contrib.auth import get_user_model

class WalletRetrieveUpdateDestroyAdminAPIView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.WalletDetailsModelSerializer
    # queryset = models.Wallet.objects.all()
    def get_object(self):
        pk = self.kwargs.get('pk', None)
        if not pk:
            raise Http404 
        ins = models. Wallet.objects.get(
            user__id=pk)
        return ins


class WalletListAdminAPIView(ListAPIView):
    pagination_class = PageNumberPagination
    pagination_class.page_size = 20
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.WalletDetailsModelSerializer
    queryset = models.Wallet.objects.all()


class WalletRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    lookup_field = None
    # queryset=models.Wallet.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.WalletDetailsModelSerializer

    def get_object(self):
        ins, created = models. Wallet.objects.get_or_create(
            user=self.request.user)
        return ins

    def put(self, request, *args, **kwargs):
        self.serializer_class = serializers.WalletSaveModelSerializer
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.serializer_class = serializers.WalletSaveModelSerializer
        return super().delete(request, *args, **kwargs)


class MobileBankRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    # queryset=models.MobileBank.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.MobileBankModelSerializer

    def get_object(self):
        wallet, created = models. Wallet.objects.get_or_create(
            user=self.request.user)
        ins, created = models.MobileBank.objects.get_or_create(wallet=wallet,)
        if created:
            ins.number = self.request.GET.get("number", "")
            ins.bankName = self.request.GET.get("bankName", "")
            ins.save()
        return ins

    def get_serializer(self, *args, **kwargs):
        kwargs["partial"] = True
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,)
        return Response(serializer.errors,)


class MobileBankRetrieveUpdateDestroyAdminAPIView(RetrieveUpdateDestroyAPIView, ListAPIView):
    pagination_class = PageNumberPagination
    pagination_class.page_size = 20
    # queryset=models.MobileBank.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.MobileBankModelSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        ins = models.MobileBank.objects.filter(wallet__pk=pk,)
        return ins

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs["pk"]
        ins = models.MobileBank.objects.get(pk=pk,)
        return ins

    def get_serializer(self, *args, **kwargs):
        kwargs["partial"] = True
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class CryptoRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    # queryset=models.Crypto.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CryptoModelSerializer

    def get_object(self):
        wallet, created = models. Wallet.objects.get_or_create(
            user=self.request.user)
        ins, created = models.Crypto.objects.get_or_create(wallet=wallet,)
        if created:
            ins.address = self.request.GET.get("address", "")
            ins.networkName = self.request.GET.get("networkName", "")
            ins.cryptoName = self.request.GET.get("cryptoName", "")
            ins.save()
        return ins

    def get_serializer(self, *args, **kwargs):
        kwargs["partial"] = True
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,)
        return Response(serializer.errors,)


class CryptoRetrieveUpdateDestroyAdminAPIView(RetrieveUpdateDestroyAPIView, ListAPIView):
    pagination_class = PageNumberPagination
    pagination_class.page_size = 20
    # queryset=models.Crypto.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.CryptoModelSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        ins = models.Crypto.objects.filter(wallet__pk=pk,)
        return ins

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs["pk"]
        ins = models.Crypto.objects.get(pk=pk,)
        return ins

    def get_serializer(self, *args, **kwargs):
        kwargs["partial"] = True
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class BankAccountRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.BankAccountModelSerializer

    def get_object(self):
        wallet, created = models. Wallet.objects.get_or_create(
            user=self.request.user)
        ins, created = models.BankAccount.objects.get_or_create(wallet=wallet,)
        if created:
            ins.accountNumber = self.request.GET.get("accountNumber", "")
            ins.accountHolderName = self.request.GET.get(
                "accountHolderName", "")
            ins.bankName = self.request.GET.get("bankName", "")
            ins.branchName = self.request.GET.get("branchName", "")
            ins.save()
        return ins

    def get_serializer(self, *args, **kwargs):
        kwargs["partial"] = True
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,)
        return Response(serializer.errors,)


class BankAccountRetrieveUpdateDestroyAdminAPIView(RetrieveUpdateDestroyAPIView, ListAPIView):
    pagination_class = PageNumberPagination
    pagination_class.page_size = 20
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.BankAccountModelSerializer

    def get_queryset(self):
        pk = self.kwargs["pk"]
        ins = models.BankAccount.objects.filter(wallet__pk=pk,)
        return ins

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs["pk"]
        ins = models.BankAccount.objects.get(pk=pk,)
        return ins

    def get_serializer(self, *args, **kwargs):
        kwargs["partial"] = True
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class WithDrawRequestAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data.dict()
        except:
            data=dict(request.data)
        data["user"] = request.user.id
        withdrawalReq = models.WithdrawalRequest()
        created,d = withdrawalReq.saveFromData(data)
        if not created:
            return Response({"msg":"Sorry"},status=401)
        _data=d.data()
        data["withdrawalRequest"] = _data["id"]
        if _data["type"] == "MobileBank":
            created,_ = models.MobileBankWithdrawalRequet().saveFromData(data)
        elif _data["type"] == "Bank":
            created,_ = models.BankWithdrawalRequet().saveFromData(data)
        elif _data["type"] == "Crypto":
            created,_ = models.CryptoWithdrawalRequet().saveFromData(data)
        if created:
            return Response({"msg":"Successfully Request send"},status=200)
        else:
            return Response({"msg":"Sorry"},status=401)


class WithDrawRequestListAPIView(ListAPIView):
    queryset = models.WithdrawalRequest.objects.all().order_by("-created_at")
    serializer_class = serializers.WithdrawalRequestDetailsModelSerializer
    # pagination_class = PageNumberPagination
    # pagination_class.page_size = 20
    permission_classes = [permissions.IsAdminUser]


class WithDrawRequestListFilterAPIView(ListAPIView):
    # queryset=models.WithdrawalRequest.objects.all()
    serializer_class = serializers.WithdrawalRequestDetailsModelSerializer
    # pagination_class = PageNumberPagination
    # pagination_class.page_size = 20
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        # MobileBank,Bank,Crypto
        type_ = self.kwargs["type"]
        queryset = models.WithdrawalRequest.objects.filter(type=type_).order_by("-created_at")
        print(queryset)
        return queryset


class WithDrawRequestUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.WithdrawalRequest.objects.all()
    serializer_class = serializers.WithdrawalRequestSaveSerializer
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, *args, **kwargs):
        data = request.data
        print(data)
        status = data.get("status", None)
        if status == "Accepted":
            amount = data.get("amount", None)
            if amount:
                amount_decimal = Decimal(amount)
                pk = kwargs["pk"]
                wq = models.WithdrawalRequest.objects.get(id=pk)
                if wq.status == status:
                    return Response({"error": "Request already accepted."}, status=400)
                user = wq.user
                if user.bgcoin < amount_decimal:
                    return Response({"error": "Insuffucient balance."}, status=400)
                user.bgcoin -= amount_decimal
                user.save()
                return self.partial_update(request, *args, **kwargs)
            else:
                return Response({"error": "Please send withdrawal amount."}, status=400)
        return self.partial_update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        data = request.data
        print(data)
        status = data.get("status", None)
        if status == "Accepted":
            amount = data.get("amount", None)
            if amount:
                amount_decimal = Decimal(amount)
                pk = kwargs["pk"]
                wq = models.WithdrawalRequest.objects.get(id=pk)
                if wq.status == status:
                    return Response({"error": "Request already accepted."})
                user = wq.user
                if user.bgcoin < amount_decimal:
                    return Response({"error": "Insuffucient balance."})
                user.bgcoin -= amount_decimal
                user.save()
            else:
                return Response({"error": "Please send withdrawal amount."}, status=422)
        return super().patch(request, *args, **kwargs)
