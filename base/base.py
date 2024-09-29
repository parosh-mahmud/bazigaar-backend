from django.db.models import base
from rest_framework.serializers import ModelSerializer

class DefaultModelSerializer(ModelSerializer):
    class Meta:
        model=None
        fields="__all__"

class SerializedModel:
    def get_serializer_class(self,fields="__all__",exclude=None,):
        class DefaultModelSerializer(ModelSerializer):
            class Meta:
                model=None
        seri_model=DefaultModelSerializer
        seri_model.Meta.model=self.__class__
        if not exclude:      
            seri_model.Meta.fields=fields
        else:
            seri_model.Meta.exclude=exclude
        return seri_model

    def saveFromData(self,data,partial=True,fields="__all__",exclude=None,):
        seri_model=self.get_serializer_class(fields=fields,exclude=exclude)
        serializer=seri_model(self,data=data,partial=partial)
        if serializer.is_valid():
            return True,serializer.save()
        return False,serializer.errors

    def data(self,fields="__all__",exclude=None,):
        seri_class=self.get_serializer_class(fields=fields,exclude=exclude,)
        serializer=seri_class(self)
        return serializer.data


def imageToUrl(request,image):
    
    host=request.headers["Host"]
    return f"{request.scheme}://{request.get_host()}{image.url}"