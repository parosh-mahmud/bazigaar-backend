from rest_framework import serializers

from .models import *


# slider
class SliderSerializers(serializers.HyperlinkedModelSerializer):
    sliderImage = serializers.ImageField(required=False)
    class Meta:
        model = SliderModel
        fields = '__all__'
        expandable_fields = {
            'sliderImage': ('reviews.ImageSerializer', {'many': True}),
        }
        def validate(self, attrs):
            title = attrs.get('title','')
            return attrs
        def create(self, validated_data):
            return SliderModel.objects.create_user(**validated_data)

class ViewSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderModel
        fields ='__all__'