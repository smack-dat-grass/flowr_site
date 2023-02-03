from django.contrib import admin
from .models import Task, Schedule, TaskSchedule, TaskResult
# Register your models here.
admin.site.register(Task)
admin.site.register(Schedule)
admin.site.register(TaskSchedule)
admin.site.register(TaskResult)

