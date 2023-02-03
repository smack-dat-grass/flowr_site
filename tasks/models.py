from django.db import models
from datetime import datetime
from django.utils.timezone import now
from config.models import CodeModel
# Create your models here.

class Task(CodeModel):
    type= models.CharField(default='user', choices=(("system","system"), ('user', 'user')), max_length=50)

    def __str__(self):
        return f"{self.name}: {self.description}"
class Schedule(models.Model):
    name= models.CharField(max_length=50, null=False)
    type= models.CharField(max_length=70,default="adhoc", choices=(("adhoc", "adhoc"), ("minutely","minutely"), ("hourly", "hourly"), ("daily","daily")), null=False)
    attributes = models.TextField(null=False)

    def __str__(self):
        return self.name
class TaskSchedule(models.Model):
    name=models.CharField(null=False, max_length=150)
    task=models.ForeignKey(Task, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    def __str__(self):
        return f'Task Schedule for {self.task.name}'
class TaskResult(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=now)
    completion_time = models.DateTimeField(null=True)
    messages = models.TextField(null=True, default="[]")
    errors = models.TextField(null=True, default="[]" )
    results=models.TextField(null=True,default="{}")
    status =models.CharField(choices=(('Running', 'Running'),('Completed', 'Completed'), ('Completed With Errors', 'Completed With Errors')), default='Running', max_length=150)

    def __str__(self):
        return f'{self.task.name} {str(self.start_time)} {self.status}'