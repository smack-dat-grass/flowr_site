from django.db import models
from locations.models import City
# Create your models here.
class Dispensary(models.Model):
    name=models.CharField(max_length=150, null=False)
    city=models.ManyToManyField(City)
    url=models.CharField(max_length=500,default='', null=False)
    image = models.CharField(max_length=500, null=True)
    def __str__(self):
        return f"{self.name}"#, {str(self.city.state)}"