from django.contrib import admin
from . import models

admin.site.register([models.BankTransfer,
                     models.CryptoCurrency,
                     models.MobileBanking,
                     models.PaymentRequestInBankTransfer,
                     models.PaymentRequestInCryptoCurrency,
                     models.PaymentRequestInMobileBanking])