from .models import ReportHistory
from datetime import datetime
from alerts.models import Alert, Notification
import json
from django.utils import timezone
# 2021-04-18 19:04:11.804550
date_formats = ['%Y-%m-%d %H:%M:%S.%f','%Y-%m-%d %H:%M:%S']#probably a better way to do this

#this file contains helper functions for report alerting
def record_count_greater_than(report, count):
    return len(json.loads(ReportHistory.objects.filter(report=report).order_by('-creation_date')[0].data)) > count
def record_count_less_than(report, count):
    return len(json.loads(ReportHistory.objects.filter(report=report).order_by('-creation_date')[0].data)) < count
def record_count_greater_than_equal_to(report, count):
    return len(json.loads(ReportHistory.objects.filter(report=report).order_by('-creation_date')[0].data)) >= count
def record_count_less_than_equal_to(report, count):
    return len(json.loads(ReportHistory.objects.filter(report=report).order_by('-creation_date')[0].data)) <= count
def report_has_entries_older_than(report,column, days):
    report_history = json.loads(ReportHistory.objects.filter(report=report).order_by('-creation_date')[0].data)
    for str_format in date_formats:
        try:
            #try to review the report, if hte date format is wrong we should throw an exception and move on
            for i in range(1, len(report_history)):
                d = datetime.strptime(report_history[i][column], str_format)
                if (datetime.now() - d).days > days:
                    print("returning true")
                    return True
        except:
            continue

    return False
def clear_alerts(name):

    for alert in Alert.objects.filter(name=name, active=True):
        alert.active=False
        alert.save()
def clear_notifications(name):

    for notification in Notification.objects.filter(name=name):

        notification.expiration_date=timezone.now()
        notification.save()
# def record_count_greater_than():
#     pass
# def record_count_greater_than():
#     pass
# def record_count_greater_than():
#     pass
# def record_count_greater_than():
#     pass
# def record_count_greater_than():
#     pass