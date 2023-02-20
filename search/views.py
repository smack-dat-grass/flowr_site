from django.shortcuts import render
import json,os
# Create your views here.
# from .functions import random_color, run_report as run_report_task, build_chartjs_line_data, build_chartjs_bar_data, build_chartjs_pie_data,build_tabulator_basic_data
# from .models import Report, ReportHistory, ReportSchedule
# from config.models import Connection
# from config.classes import OracleConnector
# from config.encryption import encrypt_message, decrypt_message
from .functions import run_search as rs
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import ObjectType
# from datetime import  datetime
from django.template import loader
# from .classes import  Workbook
# from django.http import FileResponse
from django.contrib import messages
from flowr_site.decorators import requires_password_reset
@requires_password_reset
def index(request):
    template = loader.get_template('search/index.html')
    # reports= Report.objects.all().order_by('name')
    # print(reports)
    context = {'object_types':ObjectType.objects.all().order_by("name")}
    #     'reports': reports,
    # }
    return HttpResponse(template.render(context, request))
@requires_password_reset
def results(request):
    print(request.POST)
    if 'type' not in request.POST and 'search_query' not in request.POST:
        return HttpResponseRedirect('/search/')
    template = loader.get_template('search/results.html')
    _type=request.POST['type']
    _query=request.POST['search_query']
    print(f"{_type} {_query}")
    # run_search(_query, ObjectType.objects.get(name=_type))
    context = {"type":request.POST['type'],"query":request.POST['search_query']}
    #     'reports': reports,
    # }
    return HttpResponse(template.render(context, request))

def run_search(request, query,_type):
    response = {}
    try:

        response['status'] = 'success'
        result = rs(query, ObjectType.objects.get(name=_type))
        response['message'] = {}
        response['warnings'] = []
        for k,v in result.items():
            if k !='warnings':
                response['message'][k]=v
            else:
                response['warnings'] = v


    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
    return JsonResponse(response, content_type='application/javascript')

    pass

def get_description(request, _type):
    response = {}
    try:

        response['status'] = 'success'
        response['message'] = ObjectType.objects.get(name=_type).description

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
    return JsonResponse(response, content_type='application/javascript')