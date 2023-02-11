from django.db import models
from django.utils.timezone import now
# Create your models here.
class State(models.Model):
    name=models.CharField(max_length=150, null=False)
    code=models.CharField(max_length=3, null=False)
    legal=models.BooleanField(default=False, null=False)
    creation_date = models.DateTimeField(null=False, default=now)
    def __str__(self):
        return self.name
class City(models.Model):
    name=models.CharField(max_length=150, null=False)
    state=models.ForeignKey(State,null=False,on_delete=models.RESTRICT)
    creation_date = models.DateTimeField(null=False, default=now)
    last_refreshed = models.DateTimeField(null=False, default=now)
    def __str__(self):
        return f"{self.name}, {self.state.code}"

class Location(models.Model):
    # name=models.CharField(max_length=150, null=False)
    state=models.ForeignKey(State,null=False,on_delete=models.RESTRICT)
    city=models.ForeignKey(City,null=False,on_delete=models.RESTRICT)
    def __str__(self):
        return f"{self.name}, {self.state.code}"