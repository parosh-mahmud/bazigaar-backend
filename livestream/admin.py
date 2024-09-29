from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.LiveStream)
admin.site.register(models.Comment)
admin.site.register(models.Reaction)