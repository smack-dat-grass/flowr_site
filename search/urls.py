from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('<str:query>/<str:_type>/run_search', views.run_search, name='run_search'),
    path('<str:_type>/get_description', views.get_description, name='get_description'),
    # path('<int:report_id>/getjsreport', views.getjsreport, name='getjsreport'),
    # path('<int:report_id>/run', views.run_report, name='run_report'),
    # path('test/', views.test, name='test_shit'),
    # path('download_reports/', views.download_reports, name='download_reports'),
]