from rest_framework.generics import ListAPIView
from . import models
from rest_framework import permissions
from .faq_dict_list import faq_list

class FAQList(ListAPIView):
    serializer_class=models.FAQ().get_serializer_class()
    permission_classes=[
        permissions.AllowAny
    ]
    queryset=models.FAQ.objects.all()
    
    def get_queryset(self):
        query_params = self.request.query_params
        q=query_params["q"]
        queryset=super().get_queryset()
        count=queryset.count()
        if count<=0:
            for faq in faq_list:
                models.FAQ().saveFromData(faq)
            queryset=models.FAQ.objects.all()
            
        if q!="All" and q!="":
            queryset=queryset.filter(
               topic__icontains=q 
            )
        return queryset