from django.db import models
# from locations.models import City
# Create your models here.
from django.utils.timezone import now
from dispensaries.models import Dispensary
from products.classes import ProductType
# dispensary = ""
#     producer = ""
#     name = ""
#     type = ""
#     thc = ""
#     quantity = ""
#     price = ""
#     raw = ""
class Product(models.Model):
    producer=models.CharField(max_length=150, null=False)
    dispensary=models.ForeignKey(Dispensary,on_delete=models.RESTRICT )
    name=models.CharField(max_length=150, null=False)
    type=models.CharField(max_length=50,choices=((ProductType.FLOWER,ProductType.FLOWER), (ProductType.EDIBLES,ProductType.EDIBLES), (ProductType.VAPORIZERS ,ProductType.VAPORIZERS),(ProductType.CONCENTRATES,ProductType.CONCENTRATES),( ProductType.SPECIALS,ProductType.SPECIALS), (ProductType.PREROLLS, ProductType.PREROLLS)), default=ProductType.FLOWER, null=False)
    thc = models.CharField(max_length=50, null=False, default="")
    quantity= models.CharField(max_length=50, null=False, default="")
    price= models.CharField(max_length=50, null=False, default="")
    raw= models.TextField(max_length=1000, null=False, default="")
     # raw=models.CharField(max_length=500,choices=((ProductType.FLOWER,ProductType.FLOWER), (ProductType.EDIBLES,ProductType.EDIBLES), (ProductType.VAPORIZERS ,ProductType.VAPORIZERS),(ProductType.CONCENTRATES,ProductType.CONCENTRATES),( ProductType.SPECIALS,ProductType.SPECIALS), (ProductType.PREROLLS, ProductType.PREROLLS)), default=ProductType.FLOWER, null=False)
    url=models.CharField(max_length=1000,default='', null=False)
    image = models.CharField(max_length=1000, null=True, default="")
    creation_date = models.DateTimeField(null=False, default=now)
    last_refreshed = models.DateTimeField(null=False, default=now)
    def __str__(self):
        return f"{self.name}"#, {str(self.city.state)}"