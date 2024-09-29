from django.contrib import admin

# Register your models here.
from . import models

admin.site.register([
    models.WithdrawalRequest,
    models.BankWithdrawalRequet,
    models.CryptoWithdrawalRequet,
    models.MobileBankWithdrawalRequet,
    models.Wallet,
])