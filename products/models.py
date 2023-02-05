from django.db import models
from dispensaries.models import Dispensary
# Create your models here.
class DosageTypeEnum:
    MILLIGRAM='mg'
    PERCENT='%'
    GRAM='g'
class DosageType(models.Model):
    name = models.CharField(max_length=150, null=False)

    def __str__(self):
        return self.name

class ProductType(models.Model):
    name=models.CharField(max_length=150, null=False)
    description=models.CharField(max_length=150, null=False)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=150, null=False)
    type=models.ForeignKey(ProductType,on_delete=models.RESTRICT)
    thc_content=models.IntegerField(null=False, default=1)
    dosage_type = models.ForeignKey(DosageType,on_delete=models.RESTRICT)
    price=models.CharField(max_length=150, null=False)
    quantity =models.CharField(max_length=150, null=False)
    dispensary = models.ForeignKey(Dispensary,on_delete=models.RESTRICT)
    producer= models.CharField(max_length=500, null=False)
    url= models.CharField(max_length=500, null=False)
    attributes=models.TextField(null=False, default="{}") #store json attributes about the product


    def __str__(self):
        return self.name