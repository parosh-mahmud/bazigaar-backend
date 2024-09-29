from rest_framework import serializers
from . import models
from user_app.miniserializers import UserSerializerMini


class CallSerializer(serializers.ModelSerializer):
    caller=serializers.SerializerMethodField("get_caller")
    callee=serializers.SerializerMethodField("get_callee")
    class Meta:
        model=models.Call
        fields="__all__"
    def get_caller(self,model:models.Call):
        return UserSerializerMini(model.caller,many=False).data
    def get_callee(self,model:models.Call):
        return UserSerializerMini(model.callee ,many=False).data