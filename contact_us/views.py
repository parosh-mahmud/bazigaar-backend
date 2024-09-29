from rest_framework.generics import CreateAPIView
from . import models , serializers


class CreateContactUsMessage(CreateAPIView):
    queryset = models.ContactUsMessage.objects.all()
    serializer_class = serializers.ContactUsMessageSerializer