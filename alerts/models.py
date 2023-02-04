from django.db import models

# Create your models here.
from django.db import models
# from .functions import *
from datetime import datetime
from tasks.models import Schedule
from config.models import Connection,CodeModel
from django.utils import timezone
# from datetime import datetime
# Create your models here.
from django.utils.text import slugify
from django.utils.timezone import now




#actual triggered alert
class Alert(models.Model):


    def __str__(self):
        return self.name
    #todo add scheduling piece
    name = models.CharField(max_length=100, null=False,)
    description = models.TextField(null=False, blank=False,default="Please add a description")
    resolution = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    # action = models.TextField(null=False)
    creation_date = models.DateTimeField(null=False, default=now)
    resolution_date = models.DateTimeField(null=True, blank=True)


class Notification(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    creation_date = models.DateTimeField(default=now)
    expiration_date = models.DateTimeField(default=now)
    def __str__(self):
        return self.name
class HealthCheck(CodeModel):
    def __str__(self):
        return f"{self.name}: {self.description}"

# a quick hack to pass data out of a an exec() statement
class HealthCheckMetric(models.Model):
    health_check=models.ForeignKey(HealthCheck,null=False, blank=False, on_delete=models.CASCADE)
    message=models.TextField(null=True)
    icon=models.TextField(null=True)
    successful =models.BooleanField(default=False, null=False)
    creation_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.health_check.name} {self.creation_date}"
