from django.contrib import admin
from . import models
from allauth.account.models import EmailConfirmation
# Register your models here.

admin.site.register([models.User,EmailConfirmation,models.ResetPasswordModel])