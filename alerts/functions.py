# from .models import HealthCheckMetric
# def run_health_check(health_check):
#     print('in run health_check')
#     # task_result = TaskResult()
#     # task=Task.objects.get(name=task_name)
#     # task_result.task=task
#     # task_result.status='Running'
#     # task_result.save()
#     errors = []
#     messages = []
#     results ={}
#     try:
#         print(health_check.code)
#         exec(health_check.code)
#         print(f"We ran the following healthcheck {health_check.name}")
#     except Exception as e:
#         print('we ran into an error')
#         print(str(e))
#         errors.append(str(e))
    # data=HealthCheckMetric.objects.filter(health_check=health_check).order_by('-id')[0].data
    # HealthCheckMetric.objects.filter(health_check=health_check).order_by('-id')[0].delete() #delete latest entry
    # print(f"we got sum data {data}")
    #