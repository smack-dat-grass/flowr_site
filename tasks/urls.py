from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='task_index'),
    path('<int:task_id>/run', views.run_task, name='run_task'),
    path('<int:task_id>/schedule', views.schedule_task, name='schedule_task'),
    path('<int:task_id>/view_results', views.view_results, name='view_results'),
    path('<int:task_id>/get_task_results_js', views.get_task_results_js, name='get_task_results_js'),
    path('<int:task_id>/view_result/<int:result_id>', views.view_result, name='view_result'),
    path('<str:job_id>/cancel_redis_job', views.cancel_redis_job, name='cancel_redis_job'),
    # path('<int:report_id>/getjson', views.get_report_json, name='get_report_json'),
    # path('<int:report_id>/run', views.run_report, name='run_report'),
]