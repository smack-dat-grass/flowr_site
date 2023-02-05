from django.db import models
from locations.models import Location
# Create your models here.
class Dispensary(models.Model):
    name=models.CharField(max_length=150, null=False)
    location=models.ForeignKey(Location,null=False, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}, {self.location}"