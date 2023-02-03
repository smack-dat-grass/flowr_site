from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:report_id>/get', views.get_report, name='get_report'),
    path('<int:report_id>/view_history', views.view_history, name='view_history'),
    path('<int:report_id>/view_actions', views.view_actions, name='view_actions'),
    path('<int:report_id>/view_action_history/<int:action_id>', views.view_action_history, name='view_action_history'),
    path('<int:report_id>/view_action_result/<int:history_id>', views.view_action_result, name='view_action_result'),
    path('<int:report_id>/view_history/<int:history_id>', views.view_report_history, name='view_history'),
    path('<int:report_id>/getjsreport', views.getjsreport, name='getjsreport'),
    path('<int:report_id>/getjsreport_history_list', views.getjsreport_history_list, name='getjsreport_history_list'),
    path('<int:report_id>/getjsreport_history/<int:history_id>', views.getjsreport_history, name='getjsreport'),
    path('<int:report_id>/run', views.run_report, name='run_report'),
    path('download_reports/', views.download_reports, name='download_reports'),
    path('<int:report_id>/create_report_history/', views.create_report_history, name='create_report_history'),
]