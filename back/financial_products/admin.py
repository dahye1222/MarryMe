from django.contrib import admin
from .models import DepositProduct, SavingProduct
# Register your models here.

admin.site.register(DepositProduct)
admin.site.register(SavingProduct)