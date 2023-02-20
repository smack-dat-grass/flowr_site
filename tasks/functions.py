from reports.models import Report, ReportSchedule, ReportHistory, ReportTrigger, ReportActionHistory
from reports.functions import run_report
from datetime import datetime, timezone, timedelta
from .models import Schedule, TaskResult, Task, TaskSchedule
from alerts.models import Alert, Notification
from reports.trigger_functions import *
import traceback
from django.utils.timezone import now
import json, pytz
# from alerts.functions import run_health_check
from alerts.models import HealthCheck,HealthCheckMetric

def validate_runnability(task_name):
    #here, we are going to check the schedule of hte task to see if we are eligible to run
    try:
        task = Task.objects.get(name=task_name)
        task_schedules = TaskSchedule.objects.filter(task=task)
        print(len(task_schedules))
        if len(task_schedules) > 0:
            task_results = TaskResult.objects.filter(task=task).order_by('-completion_time')
            if len(task_results) == 0:
                print(f"no task results, can be run")
                return True  # if it's never been run, run it
            latest_result = task_results[0]
            for schedule in task_schedules:
                schedule_attrs = json.loads(schedule.schedule.attributes)
                if schedule.schedule.type == 'minutely':
                    print(f"checking minutely schedule")
                    if 'interval' in schedule_attrs:#if there's an interval we need to determine the difference
                        print(f"has minutely interval")
                        print(f"Minutes since last run {(now()-latest_result.completion_time).seconds / 60}")
                        if (now()-latest_result.completion_time).seconds/60  > int(schedule_attrs['interval']): #check to see if we've exceeded the interval
                            return True
                    else:
                        print(f"has no minutely interval")
                        print(f"Minutes since last run {(now()-latest_result.completion_time).seconds / 60}")
                        if (now()-latest_result.completion_time).seconds / 60 > 1:  # no schedule means minutely
                            return True
                if schedule.schedule.type == 'hourly':
                    print(f"checking hourly schedule")
                    print(latest_result.completion_time)
                    print(now())
                    if 'interval' in schedule_attrs:  # if there's an interval we need to determine the difference
                        print(f"has hourly interval")
                        print(f"seconds since last run: {(now()-latest_result.completion_time).seconds} hours since last run {(now()-latest_result.completion_time).seconds //3600}")
                        if (now()-latest_result.completion_time).seconds //3600 > int(schedule_attrs['interval']):  # check to see if we've exceeded the interval
                            return True
                    else:
                        print(f"has no hourly interval")
                        print(f"seconds since last run: {(now()-latest_result.completion_time).seconds} hours since last run {(latest_result.completion_time-now()).seconds //3600}")
                        if (now()-latest_result.completion_time).seconds //3600 > 1: #no interval runs hourly
                            return True
                if schedule.schedule.type == 'daily':
                    print(f"checking daily schedule")
                    if 'interval' in schedule_attrs:  # if there's an interval we need to determine the difference
                        print("has daily interval")
                        print(f"hours since last run {(now()-latest_result.completion_time).days}")
                        if (now()-latest_result.completion_time).days > int(schedule_attrs['interval']):  # check to see if we've exceeded the interval
                            return True
                    else:
                        print("has no daily interval")
                        print(f"hours since last run {(now()-latest_result.completion_time).days}")
                        if (now()-latest_result.completion_time).days > 1:  # no interval means daily
                            return True


            print("didn't hit a condition")
            return False #if we haven't returned yet we return false
        else:
            return True #
    except:
        traceback.print_exc()
        return False
    pass
def run_task(task_name):
    #check the schedule
    if not validate_runnability(task_name):
        print("cannot be run right now")
        return
    task = Task.objects.get(name=task_name)
    # prelim checks to ensure there are no already running tasks for this one
    if len([x for x in TaskResult.objects.filter(task=task, status='Running')]) > 0:
        return

    task_result = TaskResult()
    task_result.creation_date = now()
    task_result.task=task
    task_result.status='Running'
    task_result.save()
    _errors = []
    try:

        _messages =[]
        try:
            print(task.code)
            exec(task.code)
            print(f"We ran the following task {task_name}")
            # _messages.append(f"Ran {task_name} successfully")

        except Exception as e:
            # import traceback
            print(traceback.format_exc())
            print('we ran into an error')
            print(traceback.format_exc())
            _errors.append(traceback.format_exc())
        if len(_errors) == 0:
            task_result.status = 'Completed'
        else:
            task_result.status = 'Completed With Errors'
        task_result.save()
        task_result = TaskResult.objects.get(id=task_result.id)
        if len(task_result.messages) > 0:
            messages = json.loads(task_result.messages)
            for x in _messages:
                messages.append(x)
            if task_result.status=='Completed':
                messages.append(f"Completed {task_name} successfully")
            task_result.messages = json.dumps(messages)
        # task_result.results = json.dumps(results)
        if len(task_result.errors) > 0:
            errors = json.loads(task_result.errors)
            for x in _errors:
                errors.append(x)
            if len(errors) >0:
                task_result.status='Completed With Errors'
            task_result.errors = json.dumps(errors)
    except:
        print(traceback.format_exc())
        _errors.append(traceback.format_exc())
        if len(task_result.errors) > 0:
            errors = json.loads(task_result.errors)
            for x in _errors:
                errors.append(x)
            if len(errors) >0:
                task_result.status='Completed With Errors'
            task_result.errors = json.dumps(errors)
        else:
            task_result.status = 'Completed With Errors'
            task_result.errors = json.dumps(_errors)

    task_result.completion_time = now()
    task_result.save()

def run_minutely_reports(task_name):
    print(f"running task {task_name}")
    print("in run minutely reports")
    task_result = TaskResult()
    task=Task.objects.get(name=task_name)
    task_result.task=task
    task_result.status='Running'
    task_result.save()
    errors = []
    messages = []
    results ={}
    schedules = Schedule.objects.filter(type='minutely')
    for schedule in schedules:
        schedule_attributes = json.loads(schedule.attributes)
        if 'interval' in schedule_attributes:
            #so now we check to see if the
            if datetime.now().minute % schedule_attributes['interval'] == 0:
                for report_schedule in ReportSchedule.objects.filter(schedule=schedule):

                    print(f"Running report for {report_schedule.report.name}")
                    try:
                        run_report(report_schedule.report)
                        check_report_trigger(report_schedule.report)
                        messages.append(f"Ran {report_schedule.report.name} successfully")

                    except Exception as e:
                        errors.append(f"Errors occurred running {report_schedule.report.name}: {traceback.format_exc()}")
            else:
                print(f"Skipping run of {schedule.name} as it is not a given interval")
    if len(errors) ==0:
        task_result.status='Completed'
    else:
        task_result.status='Completed with errors'
    task_result.messages =json.dumps(messages)
    task_result.results =json.dumps(results)
    task_result.errors =json.dumps(errors)
    task_result.completion_time = now()
    task_result.save()
def run_hourly_reports(task_name):
    print(f"running task {task_name}")
    print("in run hourly reports")
    schedules = Schedule.objects.filter(type='hourly')
    for schedule in schedules:
        schedule_attributes = json.loads(schedule.attributes)
        for report_schedule in ReportSchedule.objects.filter(schedule=schedule):
            print(f"Running report for {report_schedule.report.name}")
            run_report(report_schedule.report)
            check_report_trigger(report_schedule.report)
def load_reports_by_last_update():
    scheduled_reports = [x.report for x in ReportSchedule.objects.all().order_by('-report_id')]
    results  = [ReportHistory.objects.filter(report=x.id).order_by('-creation_date')[0] for x in scheduled_reports]
    print('\n'.join([str(x.creation_date) for x in results]))
    return results
def run_reports_lightweight(task_name, task_result):
    task = Task.objects.get(name=task_name)
    task_attrs = json.loads(task.attributes)
    print("in run reports")
    errors = []
    messages = []
    results ={}
    # print("We are now running the following reports: ")
    # print('\n'.join([x.report.name for x in ReportSchedule.objects.all().order_by('-report_id')]))
    results = [ReportSchedule.objects.get(report=x.report.id) for x in load_reports_by_last_update()][:task_attrs['count']]
    for i  in range(0, len(results)):
        report_schedule = results[i]
        print(f"Running report for {report_schedule.report.name}")
        print(f"Checking report schedule: {report_schedule.name}")
        histories = ReportHistory.objects.filter(report=report_schedule.report).order_by('-id')[:1]
        if len(histories) == 0: #if it's never been run before, just run it and move on
            try:
                run_report(report_schedule.report)
                check_report_trigger(report_schedule.report)
                # action_report(report_schedule.report)
                messages.append(f"Ran {report_schedule.report.name} successfully")
                continue
            except Exception as e:
                errors.append(f"Errors occurred running {report_schedule.report.name}: {traceback.format_exc()}")
                continue
        if report_schedule.schedule.type =='minutely': #case for minutely reports
            print('in minute part')
            schedule_attrs = json.loads(report_schedule.schedule.attributes)
            if 'interval' in schedule_attrs: #check to see if we specified an interval
                #now check if there is a report history, if so check the date of the latest and compare it
                # if datetime.now().minute % schedule_attrs['interval'] == 0: #interval is the number of minutes between runs
                #check to see   if it's been x minutes since the last run
                print(f'last report run of {report_schedule.report.name}: {str(histories[0].creation_date)}')
                print(f"Current Time: {now()} ")
                print(f" minutes since last run{int((now() - histories[0].creation_date).seconds/60)}")
                if len(histories) > 0 and int((now() - histories[0].creation_date).seconds/60) >= schedule_attrs['interval']:
                    print(f"Running report for {report_schedule.report.name}")
                    try:
                        run_report(report_schedule.report)
                        check_report_trigger(report_schedule.report)
                        # action_report(report_schedule.report)
                        messages.append(f"Ran {report_schedule.report.name} successfully")
                    except Exception as e:
                        errors.append(f"Errors occurred running {report_schedule.report.name}: {traceback.format_exc()}")
            else: #if no interval is specified, run every minute
                print(f"Running report for {report_schedule.report.name}")
                try:
                    run_report(report_schedule.report)
                    check_report_trigger(report_schedule.report)
                    # action_report(report_schedule.report)
                    messages.append(f"Ran {report_schedule.report.name} successfully")
                except Exception as e:
                    errors.append(f"Errors occurred running {report_schedule.report.name}: {traceback.format_exc()}")

        if report_schedule.schedule.type=='hourly':
            print('in hour report part')
            report_histories = ReportHistory.objects.filter(report=report_schedule.report).order_by('-id')[:1]
            schedule_attrs = json.loads(report_schedule.schedule.attributes)
            if 'interval' in schedule_attrs: #check to see if we specified an interval
                #if an interval is specified, we need to determine the number of hours since the last run of the report

                if len(report_histories) == 0:
                    #if the report has never been run go ahead and run it
                    try:
                        run_report(report_schedule.report)
                        check_report_trigger(report_schedule.report)
                        # action_report(report_schedule.report)
                        messages.append(f"Ran {report_schedule.report.name} successfully")
                    except Exception as e:
                        errors.append(f"Errors occurred running {report_schedule.report.name}: {traceback.format_exc()}")
                else:
                    #otherwise the report has run before so we need to determine the time difference between the two
                    # print()
                    delta = (now() - report_histories[0].creation_date)
                    print(f'last report run of {report_schedule.report.name}: {str(report_histories[0].creation_date)}')
                    print(f"Current Time: {now()} ")
                    print(f"Interval in seconds since last run: {delta.seconds} ")
                    print(f"Interval in days since last run: {delta.days} ")
                    print(f"Interval in hours since last run: {int(delta.seconds//3600)} ")

                    if int(delta.seconds/(60*60)) >= schedule_attrs['interval']: #if it's been the number of hours since the interval, run the report
                        try:
                            run_report(report_schedule.report)
                            check_report_trigger(report_schedule.report)
                            # action_report(report_schedule.report)
                            messages.append(f"Ran {report_schedule.report.name} successfully")
                        except Exception as e:
                            errors.append(f"Errors occurred running {report_schedule.report.name}: {traceback.format_exc()}")
                # if datetime.now().minute % schedule_attrs['interval'] == 0: #interval is the number of minutes between runs
            else: #if no interval is specified, we simply run every hour
                if len(report_histories) == 0:
                    # if the report has never been run go ahead and run it
                    try:
                        run_report(report_schedule.report)
                        check_report_trigger(report_schedule.report)
                        # action_report(report_schedule.report)
                        messages.append(f"Ran {report_schedule.report.name} successfully")
                    except Exception as e:
                        errors.append(f"Errors occurred running {report_schedule.report.name}: {traceback.format_exc()}")
                else:
                    # otherwise the report has run before so we need to determine the time difference between the two
                    delta = now() - report_histories[0].creation_date
                    print(f'last report run of {report_schedule.report.name}: {str(report_histories[0].creation_date)}')
                    if int(delta.seconds/(60*60)) >= 1:  # if it's been an hour since last run, run the report
                        try:
                            run_report(report_schedule.report)
                            check_report_trigger(report_schedule.report)
                            # action_report(report_schedule.report)
                            messages.append(f"Ran {report_schedule.report.name} successfully")
                        except Exception as e:
                            errors.append(f"Errors occurred running {report_schedule.report.name}: {traceback.format_exc()}")
        if report_schedule.schedule.type=='daily':
            print('in daily report part')
            report_histories = ReportHistory.objects.filter(report=report_schedule.report).order_by('-id')[:1]
            schedule_attrs = json.loads(report_schedule.schedule.attributes)
            if 'interval' in schedule_attrs: #check to see if we specified an interval
                #if an interval is specified, we need to determine the number of hours since the last run of the report


                #otherwise the report has run before so we need to determine the time difference between the two
                # print()
                delta = (now() - report_histories[0].creation_date)
                print(f'last report run of {report_schedule.report.name}: {str(report_histories[0].creation_date)}')
                print(f"Current Time: {now()} ")
                print(f"Interval in seconds since last run: {delta.seconds} ")
                print(f"Interval in days since last run: {delta.days} ")
                print(f"Interval in hours since last run: {int(delta.seconds//3600)} ")

                if int(delta.days) >= schedule_attrs['interval']: #if it's been the number of hours since the interval, run the report
                    try:
                        run_report(report_schedule.report)
                        check_report_trigger(report_schedule.report)
                        # action_report(report_schedule.report)
                        messages.append(f"Ran {report_schedule.report.name} successfully")
                    except Exception as e:
                        errors.append(f"Errors occurred running {report_schedule.report.name}: {traceback.format_exc()}")
            # if datetime.now().minute % schedule_attrs['interval'] == 0: #interval is the number of minutes between runs
            else: #if no interval is specified, we simply run every hour
                    # otherwise the report has run before so we need to determine the time difference between the two
                delta = now() - report_histories[0].creation_date
                print(f'last report run of {report_schedule.report.name}: {str(report_histories[0].creation_date)}')
                if int(delta.days) >= 1:  # if it's been a day since the last run of hte report, run it now
                    try:
                        run_report(report_schedule.report)
                        check_report_trigger(report_schedule.report)
                        # action_report(report_schedule.report)
                        messages.append(f"Ran {report_schedule.report.name} successfully")
                    except Exception as e:
                        errors.append(f"Errors occurred running {report_schedule.report.name}: {str()}")
    task_result.errors=json.dumps(errors)
    task_result.messages=json.dumps(messages)
    task_result.results=json.dumps(results)
    task_result.save()
def run_reports(task_name, task_result):
    print("in run reports")
    errors = []
    messages = []
    results ={}
    print("We are now running the following reports: ")
    print('\n'.join([x.report.name for x in ReportSchedule.objects.all().order_by('-report_id')]))
    for report_schedule in ReportSchedule.objects.all().order_by('-report_id'):
        print(f"Running report for {report_schedule.report.name}")
        print(f"Checking report schedule: {report_schedule.name}")
        histories = ReportHistory.objects.filter(report=report_schedule.report).order_by('-id')[:1]
        if len(histories) == 0: #if it's never been run before, just run it and move on
            try:
                run_report(report_schedule.report)
                check_report_trigger(report_schedule.report)
                # action_report(report_schedule.report)
                messages.append(f"Ran {report_schedule.report.name} successfully")
                continue
            except Exception as e:
                errors.append(f"Errors occurred running {report_schedule.report.name}: {traceback.format_exc()}")
                continue
        if report_schedule.schedule.type =='minutely': #case for minutely reports
            print('in minute part')
            schedule_attrs = json.loads(report_schedule.schedule.attributes)
            if 'interval' in schedule_attrs: #check to see if we specified an interval
                #now check if there is a report history, if so check the date of the latest and compare it
                # if datetime.now().minute % schedule_attrs['interval'] == 0: #interval is the number of minutes between runs
                #check to see   if it's been x minutes since the last run
                print(f'last report run of {report_schedule.report.name}: {str(histories[0].creation_date)}')
                print(f"Current Time: {now()} ")
                print(f" minutes since last run{int((now() - histories[0].creation_date).seconds/60)}")
                if len(histories) > 0 and int((now() - histories[0].creation_date).seconds/60) >= schedule_attrs['interval']:
                    print(f"Running report for {report_schedule.report.name}")
                    try:
                        run_report(report_schedule.report)
                        check_report_trigger(report_schedule.report)
                        # action_report(report_schedule.report)
                        messages.append(f"Ran {report_schedule.report.name} successfully")
                    except Exception as e:
                        errors.append(f"Errors occurred running {report_schedule.report.name}: {traceback.format_exc()}")
            else: #if no interval is specified, run every minute
                print(f"Running report for {report_schedule.report.name}")
                try:
                    run_report(report_schedule.report)
                    check_report_trigger(report_schedule.report)
                    # action_report(report_schedule.report)
                    messages.append(f"Ran {report_schedule.report.name} successfully")
                except Exception as e:
                    errors.append(f"Errors occurred running {report_schedule.report.name}: {traceback.format_exc()}")

        if report_schedule.schedule.type=='hourly':
            print('in hour report part')
            report_histories = ReportHistory.objects.filter(report=report_schedule.report).order_by('-id')[:1]
            schedule_attrs = json.loads(report_schedule.schedule.attributes)
            if 'interval' in schedule_attrs: #check to see if we specified an interval
                #if an interval is specified, we need to determine the number of hours since the last run of the report

                if len(report_histories) == 0:
                    #if the report has never been run go ahead and run it
                    try:
                        run_report(report_schedule.report)
                        check_report_trigger(report_schedule.report)
                        # action_report(report_schedule.report)
                        messages.append(f"Ran {report_schedule.report.name} successfully")
                    except Exception as e:
                        errors.append(f"Errors occurred running {report_schedule.report.name}: {traceback.format_exc()}")
                else:
                    #otherwise the report has run before so we need to determine the time difference between the two
                    # print()
                    delta = (now() - report_histories[0].creation_date)
                    print(f'last report run of {report_schedule.report.name}: {str(report_histories[0].creation_date)}')
                    print(f"Current Time: {now()} ")
                    print(f"Interval in seconds since last run: {delta.seconds} ")
                    print(f"Interval in days since last run: {delta.days} ")
                    print(f"Interval in hours since last run: {int(delta.seconds//3600)} ")

                    if int(delta.seconds/(60*60)) >= schedule_attrs['interval']: #if it's been the number of hours since the interval, run the report
                        try:
                            run_report(report_schedule.report)
                            check_report_trigger(report_schedule.report)
                            # action_report(report_schedule.report)
                            messages.append(f"Ran {report_schedule.report.name} successfully")
                        except Exception as e:
                            errors.append(f"Errors occurred running {report_schedule.report.name}: {traceback.format_exc()}")
                # if datetime.now().minute % schedule_attrs['interval'] == 0: #interval is the number of minutes between runs
            else: #if no interval is specified, we simply run every hour
                if len(report_histories) == 0:
                    # if the report has never been run go ahead and run it
                    try:
                        run_report(report_schedule.report)
                        check_report_trigger(report_schedule.report)
                        # action_report(report_schedule.report)
                        messages.append(f"Ran {report_schedule.report.name} successfully")
                    except Exception as e:
                        errors.append(f"Errors occurred running {report_schedule.report.name}: {traceback.format_exc()}")
                else:
                    # otherwise the report has run before so we need to determine the time difference between the two
                    delta = now() - report_histories[0].creation_date
                    print(f'last report run of {report_schedule.report.name}: {str(report_histories[0].creation_date)}')
                    if int(delta.seconds/(60*60)) >= 1:  # if it's been an hour since last run, run the report
                        try:
                            run_report(report_schedule.report)
                            check_report_trigger(report_schedule.report)
                            # action_report(report_schedule.report)
                            messages.append(f"Ran {report_schedule.report.name} successfully")
                        except Exception as e:
                            errors.append(f"Errors occurred running {report_schedule.report.name}: {traceback.format_exc()}")
        if report_schedule.schedule.type=='daily':
            print('in daily report part')
            report_histories = ReportHistory.objects.filter(report=report_schedule.report).order_by('-id')[:1]
            schedule_attrs = json.loads(report_schedule.schedule.attributes)
            if 'interval' in schedule_attrs: #check to see if we specified an interval
                #if an interval is specified, we need to determine the number of hours since the last run of the report


                #otherwise the report has run before so we need to determine the time difference between the two
                # print()
                delta = (now() - report_histories[0].creation_date)
                print(f'last report run of {report_schedule.report.name}: {str(report_histories[0].creation_date)}')
                print(f"Current Time: {now()} ")
                print(f"Interval in seconds since last run: {delta.seconds} ")
                print(f"Interval in days since last run: {delta.days} ")
                print(f"Interval in hours since last run: {int(delta.seconds//3600)} ")

                if int(delta.days) >= schedule_attrs['interval']: #if it's been the number of hours since the interval, run the report
                    try:
                        run_report(report_schedule.report)
                        check_report_trigger(report_schedule.report)
                        # action_report(report_schedule.report)
                        messages.append(f"Ran {report_schedule.report.name} successfully")
                    except Exception as e:
                        errors.append(f"Errors occurred running {report_schedule.report.name}: {traceback.format_exc()}")
            # if datetime.now().minute % schedule_attrs['interval'] == 0: #interval is the number of minutes between runs
            else: #if no interval is specified, we simply run every hour
                    # otherwise the report has run before so we need to determine the time difference between the two
                delta = now() - report_histories[0].creation_date
                print(f'last report run of {report_schedule.report.name}: {str(report_histories[0].creation_date)}')
                if int(delta.days) >= 1:  # if it's been a day since the last run of hte report, run it now
                    try:
                        run_report(report_schedule.report)
                        check_report_trigger(report_schedule.report)
                        # action_report(report_schedule.report)
                        messages.append(f"Ran {report_schedule.report.name} successfully")
                    except Exception as e:
                        errors.append(f"Errors occurred running {report_schedule.report.name}: {str()}")
    task_result.errors=json.dumps(errors)
    task_result.messages=json.dumps(messages)
    task_result.results=json.dumps(results)
    task_result.save()

def check_report_trigger(report):
    if report.alert_trigger is not None:
        try:
            #queue up some variables
            alert_triggered= False #set to true in alert trigger
            report_history = ReportHistory.objects.filter(report=report).order_by('-creation_date')[0] #just doing this here so it's easier to reference
            print(report.alert_trigger.code)
            exec(report.alert_trigger.code)
            print(f"We ran the following trigger {report.alert_trigger.name}")
                   # name = models.CharField(max_length=100, null=False)
                #     resolution = models.TextField()
                #     active = models.BooleanField(default=False)
                #     action = models.TextField(null=False)
                #     creation_date = models.DateTimeField(null=True, default=now())
                #     resolution_date = models.DateTimeField(null=True)
                #     trigger = models.ForeignKey(ReportAlertTrigger,null=False, on_delete=models.CASCADE)



        except Exception as e:
            print('we ran into an error')
            print(traceback.format_exc())
            # errors.append(traceback.format_exc())
        pass
def create_alert(name,description):
    if len([x for x in Alert.objects.filter(name=name, active=True)]) == 0:
        alert = Alert()
        alert.name = name
        alert.description = description
        alert.active = True
        alert.save()
def action_report(report):

    if report.action is not None:
        report_action_history = ReportActionHistory()
        report_action_history.report_action = report.action
        report_action_history.status = "Running"
        report_action_history.save()
        try:
            # queue up some variables
            report_history = json.loads(ReportHistory.objects.filter(report=report).order_by('-creation_date')[0].data)  # just doing this here so it's easier to reference
            attributes = json.loads(report.action.attributes)
            print(report.action.code)
            exec(report.action.code)
            print(f"We ran the following report action {report.action.name}")
            report_action_history.status = "Completed"
            report_action_history.save()
        except Exception as e:
            create_alert(report.name, f"An error occurred actioning the report: <br><br>{str(e)}<br><br>Please resolve for a full Flowr experience")
            print(f'we ran into an error running {report.action.name}')
            print(traceback.format_exc())
            report_action_history.status = "Completed With Errors"
            report_action_history.save()
def create_notification(name, description,**kwargs ):
    notification = Notification()
    notification.name=name
    notification.description=description
    notification.expiration_date = now()+timedelta(**kwargs)
    notification.save()

def run_health_checks(task_result):
    errors = []
    messages = []
    results = []
    for health_check in HealthCheck.objects.all():
        try:
            print(health_check.code)
            exec(health_check.code)
            print(f"We ran the following healthcheck {health_check.name}")
            results.append(f"ran {health_check.name} successfully")
        except Exception as e:
            print(f'we ran into an error on {health_check.name}: {str(e)}')
            print(str(e))
            errors.append(f'we ran into an error on {health_check.name}: {str(e)}')

    task_result.errors=json.dumps(errors)
    task_result.messages=json.dumps(messages)
    task_result.results=json.dumps(results)
    task_result.save()

