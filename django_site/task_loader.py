import django_rq
from datetime import datetime
from tasks.models import Task, TaskSchedule, Schedule
from tasks.functions import function_lookup
def run():
    scheduler = django_rq.get_scheduler('default')

    for task_schedule in TaskSchedule.objects.all():
        print(f"loading task schedule {task_schedule.name}")
        if task_schedule.schedule.type =='minutely': #handle minutely tasks
            print(f"Scheduling task {task_schedule.task.name}")
            scheduler.schedule(scheduled_time=datetime.now(),  # Time for first execution, in UTC timezone
                                   func=function_lookup[task_schedule.task.calling_function],  # Function to be queued
                                   args=[task_schedule.task.name],  # Arguments passed into function when executed
                                   kwargs={},  # Keyword arguments passed into function when executed
                                   interval=60,  # Time before the function is called again, in seconds
                                   repeat=None,  # Repeat this number of times (None means repeat forever)
                                   meta={'foo': 'bar'})  # Arbitrary pickleable data on the job itself)



# task = Task.objects.get(pk=task_id)
# task_schedule = TaskSchedule.objects.get(task=task)
# if task_schedule.schedule.type == 'minutely':
#     scheduler.schedule(scheduled_time=datetime.now(),  # Time for first execution, in UTC timezone
#                        func=function_lookup[task.calling_function],  # Function to be queued
#                        args=[task.name],  # Arguments passed into function when executed
#                        kwargs={},  # Keyword arguments passed into function when executed
#                        interval=60,  # Time before the function is called again, in seconds
#                        repeat=None,  # Repeat this number of times (None means repeat forever)
#                        meta={'foo': 'bar'})  # Arbitrary pickleable data on the job itself)
    # job = scheduler.enqueue_in(time, function_lookup[task.calling_function], task.name)

