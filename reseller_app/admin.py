from django.contrib import admin

# Register your models here.
from .models import *

# admin.site.register(Reseller)
admin.site.register(TopUpRequest)
admin.site.register(ResellerHistory)
admin.site.register(TopUpRequestHistory)
admin.site.register(ResellerCoinRequest)

