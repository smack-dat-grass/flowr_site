import json
# Create your views here.
# from .models import Report, ReportHistory
import traceback
from reports.functions import build_tabulator_basic_data
from alerts.models import Notification
from reports.models import *
# from alerts.functions import run_health_check
from alerts.models import Alert,HealthCheck,HealthCheckMetric
from django.template import loader
from tasks.models import Task
from datetime import datetime, timedelta
from config.models import Configuration
from django.db import connection
from django.contrib import messages
# from config.encryption import encrypt_message, decrypt_message
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .decorators import requires_password_reset
from django_site.functions import generate_django_site_health

@requires_password_reset
def index(request):
    # test = encrypt_message("wubbalubbadubdub")
    # print(test)
    # print(decrypt_message(test))from datetime import timedelta
    #
    # Event.objects.filter(start_datetime__lte=datetime.now() + timedelta(days=1))
    # Notification.objects.filter(start_datetime__gte=datetime.now())
    template = loader.get_template('django_site/index.html')
    print(len(Notification.objects.filter(expiration_date__gte=datetime.now())))
    health_checks=[]
    # messages.info(request, "here's your message")
    for health_check in HealthCheck.objects.all():
        if len(HealthCheckMetric.objects.filter(health_check=health_check).order_by('-creation_date')) > 0:
            health_check_metric =  HealthCheckMetric.objects.filter(health_check=health_check).order_by('-creation_date')[0]
            if not health_check_metric.successful:
                health_checks.append(health_check_metric)
    print(health_checks)
    #07.26.22 adding code to pull report statuses
    data_dict=  {"health_checks":health_checks,"reports":Report.objects.all(), "tasks":Task.objects.all(),"alerts":Alert.objects.filter(active=True), "notifications":Notification.objects.filter(expiration_date__gte=datetime.now())}

    return HttpResponse(template.render(data_dict, request) )

def get_django_site_health(request):
    try:
        response = {'message': build_tabulator_basic_data(generate_django_site_health()), 'status':'success'}
        # response = {'message': 'fuckeryduckery', 'status':'success'}
        pass
        # health_objects=generate_ops_dashboard_health()
        # for x in data_dict['health_violators']:
        #     print(x)
    except:
        response = {'message':traceback.format_exc(), 'status':'error'}
        traceback.print_exc()


    return JsonResponse(response,content_type='application/javascript')

def handler404(request, exception, template_name="django_site/404.html"):
    template = loader.get_template(template_name)
    return HttpResponse(template.render({}, request) )

def handler500(request, template_name="django_site/500.html"):
    return HttpResponse(loader.get_template(template_name).render({}),request)

def redirect(request,path):
    #this is a hack but it should work
    # print(path)
    # print("/"+path.replace('_','/'))
    return HttpResponseRedirect(path.replace(':','/'))