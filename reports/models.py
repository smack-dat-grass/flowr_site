from django.db import models
# from django.contrib.auth import Group
# from .functions import *
from .encrypt import encrypt
from datetime import datetime
from tasks.models import Schedule
from config.models import Connection,CodeModel
from alerts.models import Alert
from django.utils import timezone
# from datetime import datetime
# Create your models here.
from django.utils.text import slugify
from django.utils.timezone import now
from taggit.managers import TaggableManager


#basically a coupler between Report and and Alert
class ReportTrigger(CodeModel):
    def __str__(self):
        return f"{self.name}: {self.description}"
    # alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
#actual triggered alert
class ReportCategory(models.Model):
    name = models.CharField(max_length=100, null=False)
    creation_date = models.DateTimeField(null=True, default=now)
    def __str__(self):
        return self.name

#the action to take on the report, passing report history. only called when scheduled
class ReportAction(CodeModel):
    # name= models.CharField(max_length=150, null=False)
    # creation_date = models.DateTimeField(default=now())
    # attributes=models.TextField(null=False, default='{}', help_text='json attributes')
    # code=models.TextField(null=True, help_text='Python Code To Execute')
    def __str__(self):
        return f"{self.name}: {self.description}"


class ReportActionHistory(models.Model):
    creation_date = models.DateTimeField(default=now)
    attributes = models.TextField(null=False, default='{}', help_text='json attributes')
    status = models.CharField(choices=(('Running', 'Running'), ('Completed', 'Completed'), ('Completed With Errors', 'Completed With Errors')),default='Running', max_length=150)
    report_action=models.ForeignKey(ReportAction,null=False, blank=True,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.report_action.name} {self.status} {self.creation_date}"
class Report(CodeModel):
    short_name=models.CharField(max_length=25, default="report_name", help_text="the short name of the report (used when downloading multiple reports)")
    creation_date = models.DateTimeField(null=True, default=now)
    connection = models.ForeignKey(Connection,blank=False, null=True, on_delete=models.CASCADE)
    code = models.TextField(null=False)
    type = models.CharField(null=False, default='basic', max_length=50)
    xaxis_label = models.CharField(null=True,blank=True,max_length=50)
    yaxis_label = models.CharField(null=True,blank=True,max_length=50)
    attributes = models.TextField(default='{}')
    alert_trigger =models.ForeignKey(ReportTrigger,null=True,blank=True, on_delete=models.CASCADE)
    group = models.ForeignKey("auth.Group", null=True, blank=True,on_delete=models.CASCADE)
    action = models.ForeignKey(ReportAction, null=True, blank=True,on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return f"{self.name}: {self.description}"

    #todo add scheduling piece
    #schedule = models.Choices(choices=(("), ("Hourly", "Hourly"),("Daily", "Daily")))



class ReportHistory(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(null=False, default=now)
    data = models.TextField()
    def __str__(self):
        return str(f"{self.report.name} {self.creation_date}")
class ReportSchedule(models.Model):
    name=models.CharField(max_length=50, null="False")
    creation_date = models.DateTimeField(null=True, default=now)
    report=models.ForeignKey(Report, on_delete=models.RESTRICT)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
