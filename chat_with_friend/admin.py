from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Message)
admin.site.register(models.ChatWithFriend)
admin.site.register(models.ImageMessage)
admin.site.register(models.Reaction)