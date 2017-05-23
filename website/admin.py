from django.contrib import admin

from .models import Product, ProductType, PaymentType, Order

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(PaymentType)
admin.site.register(Order)

