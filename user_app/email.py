from allauth.account.adapter import DefaultAccountAdapter
from django.utils.crypto import get_random_string
from django.contrib.sites.shortcuts import get_current_site
from allauth.account.models import EmailConfirmation
from django.db.models import Q
import random
from django.utils import timezone
from allauth.utils import email_address_exists
from django import forms

class ModifiedAccountAdapter(DefaultAccountAdapter):
    def generate_emailconfirmation_key(self, email):
        EmailVerifyCode = random.randint(100000,999999)
        key = EmailVerifyCode
        self.EmailVerifyCode=EmailVerifyCode
        return key
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = get_current_site(request)
        EmailVerifyCode = random.randint(100000,999999)
        # new_emailconfirmation=EmailConfirmation()
        # new_emailconfirmation.email_address=emailconfirmation.email_address
        # new_emailconfirmation.key=str(EmailVerifyCode)
        # emailconfirmation.delete()
        # new_emailconfirmation.save()
        confirmations = EmailConfirmation.objects.filter(
                Q(email_address=emailconfirmation.email_address) & Q(key=emailconfirmation.key)
            )
        if(confirmations.exists()):
            confirmation=confirmations[0]
            confirmation.key=str(EmailVerifyCode)
            confirmation.save()
        
            
        else :
            confirmation=EmailConfirmation()
            confirmation.key=str(EmailVerifyCode)
            confirmation.email_address=emailconfirmation.email_address
            confirmation.save()
        activate_url = self.get_email_confirmation_url(request, confirmation)
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": confirmation.key,
        }
        print(ctx)
        confirmation.sent = timezone.now()
        confirmation.save()
        
        if signup:
            email_template = "account/email/email_confirmation_signup"
        else:
            email_template = "account/email/email_confirmation"
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)
    def validate_unique_email(self, email):
        if email_address_exists(email):
            
            if email.verified:
                raise forms.ValidationError(self.error_messages["email_taken"])
            else :
                user=email.user
                user.delete()
        return email
