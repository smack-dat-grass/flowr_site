from config.models import Connection
from django.db import models
from locations.models import City
# Create your models here.
from django.utils.timezone import now
class Dispensary(models.Model):
    name=models.CharField(max_length=150, null=False)
    city=models.ManyToManyField(City)
    url=models.CharField(max_length=500,default='', null=False)
    image = models.CharField(max_length=500, null=True)
    connection = models.ForeignKey(Connection, on_delete=models.RESTRICT)
    creation_date = models.DateTimeField(null=False, default=now)
    last_refreshed = models.DateTimeField(null=False, default=now)

    def __str__(self):
        return f"{self.name}"#, {str(self.city.state)}"