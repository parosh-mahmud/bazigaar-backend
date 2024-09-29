from django.db import models

# Create your models here.
# class Host(models.Model):
#     user=models.ForeignKey(get_user_model(),on_delete=models.PROTECT,)
#     resellerId=models.CharField(max_length=16,unique=True)
#     # whatsappNumber=models.CharField(max_length=20,blank=True,null=True)
#     created_at=models.DateTimeField(auto_now_add=True)
#     update_at=models.DateTimeField(auto_now=True)
    
#     def __str__(self) :
#         return self.resellerId