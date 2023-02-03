import json
# Create your views here.
# from .functions import random_color, run_report as run_report_task, build_chartjs_line_data, build_chartjs_bar_data, build_chartjs_pie_data
# from .models import Report, Connection, ReportHistory
# from .classes import OracleConnector
from django.conf import settings

from .models import Task, TaskSchedule, Schedule, TaskResult
from django.http import HttpResponse, JsonResponse
from redis import Redis
from rq import Queue
import django_rq
from rq_scheduler import Scheduler
from datetime import datetime, timedelta
from django.template import loader
from .functions import  run_task as run_reddis_task
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
# Create your views here.
from config.decorators import can_access_url
from django.contrib.auth.decorators import login_required
from django_site.decorators import requires_password_reset
from reports.functions import build_tabulator_basic_data
@login_required(login_url='/accounts/login')
@can_access_url
@requires_password_reset
def index(request):
    scheduler = Scheduler(connection=Redis(settings.RQ_QUEUES['default']['HOST']))  # Get a scheduler for the "default" queue
    template = loader.get_template('tasks/index.html')
    queue = django_rq.get_queue('default')
    # queue.
    context = {"queued_tasks":[x for x in scheduler.get_jobs()], "tasks":[]}
    for task  in Task.objects.all():
        t = {'task':task,'scheduled':False}
        # context["tasks"].append(task)
        for job in scheduler.get_jobs():

            if 'task' in job.meta and job.meta['task'] == task.name:
                t['scheduled']=True
                break
        context['tasks'].append(t)
    # print(context)
    # print([x.__dict__.keys() for x in scheduler.get_jobs()])
    return HttpResponse(
        # template.render({"queued_tasks": [x.__dict__.keys() for x in scheduler.get_jobs()], "tasks": Task.objects.all()}, request))

        template.render(context, request))

@login_required(login_url='/accounts/login')
@can_access_url
@requires_password_reset
def cancel_redis_job(request, job_id):
    scheduler = Scheduler(connection=Redis(settings.RQ_QUEUES['default']['HOST']))  # Get a scheduler for the "default" queue
    for job in scheduler.get_jobs():
        if job.id == job_id:
            scheduler.cancel(job)
            print(f'cancelled job {job_id}')

    return redirect(reverse('task_index'))
@login_required(login_url='/accounts/login')
@can_access_url
@requires_password_reset
def run_task(request, task_id):
    template = loader.get_template('tasks/index.html')
    scheduler = Scheduler(connection=Redis(settings.RQ_QUEUES['default']['HOST']))  # Get a scheduler for the "default" queue
    queue = django_rq.get_queue('default')
    task = Task.objects.get(pk=task_id)
    queue.enqueue(run_reddis_task, task.name)
    messages.info(request, f"{task.name} has been started")
    return redirect(reverse('task_index'))

@login_required(login_url='/accounts/login')
@can_access_url
@requires_password_reset
def view_results(request, task_id):
    template = loader.get_template('tasks/view_results.html')
    task=Task.objects.get(id=task_id)
    context={'task_results':TaskResult.objects.filter(task=task).order_by('-completion_time')[:3000],'task':task}
    return HttpResponse(template.render(context, request))
    # template.render({"queued_tasks": [x.__dict__.keys() for x in scheduler.get_jobs()], "tasks": Task.objects.all()}, request))

    pass


@login_required(login_url='/accounts/login')
@can_access_url
@requires_password_reset
def get_task_results_js(request, task_id):

    data = [["Start Time", "Completion Time", "Status", "Action"]]
    for task in TaskResult.objects.filter(task=Task.objects.get(id=task_id)).order_by('-completion_time')[:500]:
        data.append([task.start_time, task.completion_time,task.status, f'<button class="w3-blue w3-hover-black w3-round"><a href="/tasks/{ task.task.id}/view_result/{task.id}">view</a></button>'])

    # response =
    print(len(data))
    response = {'message': build_tabulator_basic_data(data)}
    print(response['message'][-1])

    return JsonResponse(response, content_type='application/javascript')

@login_required(login_url='/accounts/login')
@can_access_url
@requires_password_reset
def view_result(request, task_id,result_id):
    template = loader.get_template('tasks/view_result.html')
    task=Task.objects.get(id=task_id)
    context={'task_result':TaskResult.objects.get(id=result_id),'task':task}
    return HttpResponse(template.render(context, request))
    # template.render({"queued_tasks": [x.__dict__.keys() for x in scheduler.get_jobs()], "tasks": Task.objects.all()}, request))

    pass
@login_required(login_url='/accounts/login')
@can_access_url
@requires_password_reset
def schedule_task(request, task_id):
    import django_rq
    scheduler = django_rq.get_scheduler('default')

    task = Task.objects.get(pk=task_id)
    task_schedule = TaskSchedule.objects.get(task=task)
    if task_schedule.schedule.type == 'minutely':
        scheduler.schedule(scheduled_time=timezone.now(),  # Time for first execution, in UTC timezone
                           func=run_reddis_task,  # Function to be queued
                           args=[task.name],  # Arguments passed into function when executed
                           kwargs={},  # Keyword arguments passed into function when executed
                           interval=60,  # Time before the function is called again, in seconds
                           repeat=None,  # Repeat this number of times (None means repeat forever)
                           meta={'task': task.name})  # Arbitrary pickleable data on the job itself)
        # job = scheduler.enqueue_in(time, function_lookup[task.calling_function], task.name)
        # queue.enqueue(function_lookup[task.calling_function], task.name)
    if task_schedule.schedule.type == 'hourly':
        scheduler.schedule(scheduled_time=timezone.now(),  # Time for first execution, in UTC timezone
                           func=run_reddis_task,  # Function to be queued
                           args=[task.name],  # Arguments passed into function when executed
                           kwargs={},  # Keyword arguments passed into function when executed
                           interval=60*60,  # Time before the function is called again, in seconds
                           repeat=None,  # Repeat this number of times (None means repeat forever)
                           meta={'task': task.name})  # Arbitrary pickleable data on the job itself)
        # job = scheduler.enqueue_in(time, function_lookup[task.calling_function], task.name)
        # queue.enqueue(function_lookup[task.calling_function], task.name)
        pass
    return redirect(reverse('task_index'))

# adding some comments as a test
#more testing comments