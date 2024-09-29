from . import models
from rest_framework import serializers
from user_app.miniserializers import UserSerializerMini
from .models import ResellerCoinRequest


# class CreateResellerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=models.Reseller
#         fields="__all__"

# class CreateResellerSerializerHistory(serializers.ModelSerializer):
#     class Meta:
#         model=models.ResellerHistory
#         fields="__all__"

class ResellerSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.User
        fields="__all__"

class TopUpRequestSerializer(serializers.ModelSerializer):
    reseller=serializers.SerializerMethodField("get_reseller")
    class Meta:
        model=models.TopUpRequest
        fields="__all__"
    def get_reseller(self,model:models.TopUpRequest):
        return ResellerSerializer(model.reseller,many=False).data

class TopUpRequestSerializerDetails(serializers.ModelSerializer):
    reseller=serializers.SerializerMethodField("get_reseller")
    requestFrom=serializers.SerializerMethodField("getRequestFrom")
    class Meta:
        model=models.TopUpRequest
        fields="__all__"
    def get_reseller(self,model:models.TopUpRequest):
        return ResellerSerializer(model.reseller,many=False).data
    def getRequestFrom(self,model:models.TopUpRequest):
        return UserSerializerMini(model.requestFrom,many=False).data

class TopUpRequestSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.TopUpRequest
        fields="__all__"

class TopUpRequestHistorySaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.TopUpRequestHistory
        fields="__all__"


class ResellerCoinReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResellerCoinRequest
        fields = "__all__"
        def create(self, validated_data):
            validated_data['status'] = 'pending'
            return super().create(validated_data)

class ResellerCoinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResellerCoinRequest
        fields = '__all__'
        read_only_fields = ('status',)
    def create(self, validated_data):
        # Set the 'status' field to 'pending' by default during object creation
        validated_data['status'] = 'pending'
        return super().create(validated_data)




from .models import CoinReq

class CoinReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinReq
        fields = ('request_id','amount_req', 'transaction_id', 'status','reseller',)

