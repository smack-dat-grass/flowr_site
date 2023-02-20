import json
from datetime import datetime
from reports.models import Report, ReportSchedule, ReportHistory
from tasks.models import Task, TaskSchedule, TaskResult
from flowr_site.classes import DjangoSiteHealth
def generate_flowr_site_health():
    violators = []
    violators += generate_report_health()
    violators += generate_task_health()
    violators.sort(key=lambda x: x.criticality, reverse=False)
    result = [['Name', 'Type','Schedule','Time Since Refresh','Criticality']]
    for violator in violators:
        result.append([violator.name, violator.object_type, violator.schedule, violator.delta])
        if violator.criticality < 3:
            result[-1].append(f'<p class="w3-red"> {violator.criticality }</p>')
        elif violator.criticality <=4 and violator.criticality > 2:
            result[-1].append(f'<p class="w3-yellow"> {violator.criticality}</p>')
        else:
            result[-1].append(f'<p class="w3-green"> {violator.criticality}</p>')
    return result

def generate_report_health():
    #ok so first things first we need to load the reports and their schedules
    report_schedules = ReportSchedule.objects.all()
    violators = []
    for report_schedule in report_schedules:
        schedule_attrs = json.loads(report_schedule.schedule.attributes)
        last_report_list = [x for x in ReportHistory.objects.filter(report=report_schedule.report).order_by('-creation_date')[:1]]
        if len(last_report_list) >0:
            last_report_run = last_report_list[0]
            print(last_report_run)
            tdelta = datetime.now()-last_report_run.creation_date
            # health_object = DjangoSiteHealth(object_type='Report', name=report_schedule.report.name, last_updated = last_report_run.creation_date)
            health_object = DjangoSiteHealth()
            health_object.name=report_schedule.report.name
            health_object.schedule=report_schedule.schedule.name
            health_object.object_type='Report'
            health_object.last_updated = last_report_run.creation_date
            health_object.criticality = last_report_run.report.criticality
            # days, hours, minutes = tdelta.days, tdelta.seconds // 3600, tdelta.seconds // 60 % 60seconds = duration.total_seconds()
            seconds = tdelta.total_seconds()
            hours = seconds//3600
            days = hours/24
            minutes = seconds/60


            delta_format = f"{days} day(s), {hours} hour(s), {minutes} minute(s)"
            print(delta_format)
            # health_object = DjangoSiteHealth(object_type='Report', name=report_schedule.report.name, last_updated = last_report_run.creation_date)
            if report_schedule.schedule.type=='hourly':
                # days, hours, minutes = tdelta.days, tdelta.seconds // 3600, tdelta.seconds // 60 % 60
                # print(f"Last run {last_report_run.creation_date}: Days: {days} Hours: {hours} Minutes: {minutes}")
                if hours > schedule_attrs['interval']:
                    health_object.delta = f"{hours} hour(s)"
                    violators.append(health_object)
            if report_schedule.schedule.type=='minutely':
                # days, hours, minutes = tdelta.days, tdelta.seconds // 3600, tdelta.seconds // 60 % 60
                # print(f"Last run {last_report_run.creation_date}: Days: {days} Hours: {hours} Minutes: {minutes}")
                if minutes > schedule_attrs['interval']:
                    health_object.delta = f"{minutes} minute(s)"
                    violators.append(health_object)
            if report_schedule.schedule.type=='daily':
                # days, hours, minutes = tdelta.days, tdelta.seconds // 3600, tdelta.seconds // 60 % 60
                # print(f"Last run {last_report_run.creation_date}: Days: {days} Hours: {hours} Minutes: {minutes}")
                if days > schedule_attrs['interval']:
                    health_object.delta = f"{days} day(s)"
                    violators.append(health_object)
        else:
            health_object = DjangoSiteHealth()
            health_object.name = report_schedule.report.name
            health_object.schedule = report_schedule.schedule.name
            health_object.object_type = 'Report'
            health_object.last_updated = 'N/A'
            health_object.delta = 'Never Run'
            health_object.criticality = report_schedule.report.criticality
            violators.append(health_object)
            continue
    return violators


    pass
def generate_task_health():
    task_schedules = TaskSchedule.objects.all()
    violators = []
    for task_schedule in task_schedules:
        schedule_attrs = json.loads(task_schedule.schedule.attributes)
        last_task_run = [x for x in TaskResult.objects.filter(task=task_schedule.task).order_by('-completion_time')[:1]][0]
        print(last_task_run)
        if last_task_run.completion_time is not None:
            tdelta = datetime.now() - last_task_run.completion_time
            health_object = DjangoSiteHealth()
            health_object.name = task_schedule.task.name
            health_object.schedule = task_schedule.schedule.name
            health_object.object_type = 'Task'
            health_object.last_updated = last_task_run.completion_time
            health_object.criticality = last_task_run.task.criticality
            seconds = tdelta.total_seconds()
            hours = seconds // 3600
            days = hours / 24
            minutes = seconds / 60

            delta_format = f"{days} day(s), {hours} hour(s), {minutes} minute(s)"
            # health_object = DjangoSiteHealth(object_type='Report', name=report_schedule.report.name, last_updated = last_report_run.creation_date)
            if task_schedule.schedule.type == 'hourly':
                if hours > schedule_attrs['interval']:
                    health_object.delta = f'{hours} hour(s)'
                    violators.append(health_object)
            if task_schedule.schedule.type == 'minutely':
                if minutes > schedule_attrs['interval']:
                    health_object.delta = f'{minutes} minute(s)'
                    violators.append(health_object)
            if task_schedule.schedule.type == 'daily':
                if days > schedule_attrs['interval']:
                    health_object.delta = f'{days} day(s)'
                    violators.append(health_object)
        else:
            health_object = DjangoSiteHealth()
            health_object.name = task_schedule.task.name
            health_object.schedule = task_schedule.schedule.name
            health_object.object_type = 'Task'
            health_object.last_updated='N/A'
            health_object.delta='Never Run'
            health_object.criticality=task_schedule.task.criticality
            violators.append(health_object)
            # violators.append(DjangoSiteHealth(name=task_schedule.task.name, object_type='Task', last_updated='', delta='Never run'))
            continue
        # health_object = DjangoSiteHealth(object_type='Report', name=report_schedule.report.name, last_updated = last_report_run.creation_date)

    return violators

def generate_health_check_health():
    pass