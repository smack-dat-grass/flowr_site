from django.contrib import admin
from products.models import ProductType, Product, DosageType
# Register your models here.
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(DosageType)
