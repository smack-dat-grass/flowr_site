from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Report)
admin.site.register(ReportHistory)
admin.site.register(ReportSchedule)
admin.site.register(ReportTrigger)
admin.site.register(ReportCategory)
admin.site.register(ReportAction)
admin.site.register(ReportActionHistory)


