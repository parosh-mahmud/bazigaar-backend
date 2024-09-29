from django.contrib import admin
from . import models
# Register your models here.
admin.site.register([models.Achievement,models.UserAchievement,models.UserLevel])