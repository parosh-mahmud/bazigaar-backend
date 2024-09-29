from django.contrib import admin
from . import models

admin.site.register([models.RequestNotification,
                     models.EventNotification,
                     models.GameNotification,
                     models.PromotionNotification])