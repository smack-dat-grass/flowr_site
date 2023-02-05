from django.shortcuts import render
import json,os
# Create your views here.
from django.utils import timezone

from .functions import random_color, run_report as run_report_task, build_chartjs_line_data, build_chartjs_bar_data, build_chartjs_pie_data,build_tabulator_basic_data
from .models import Report, ReportHistory, ReportSchedule, ReportAction, ReportActionHistory
from config.models import Connection
from config.classes import OracleConnector
from config.encryption import encrypt_message, decrypt_message
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from datetime import  datetime
from django.template import loader
from .classes import  Workbook
from django.contrib import messages
from django.http import FileResponse
import traceback
from dope_deals_site.decorators  import requires_password_reset
@requires_password_reset
def index(request):
    template = loader.get_template('reports/index.html')
    reports= Report.objects.all().order_by('name')
    # print(reports)
    report_schedules ={}
    for report in reports:
        _report_schedules = [x for x in ReportSchedule.objects.filter(report=report)]
        if len(_report_schedules) > 0:
            report_schedules[report.name]=_report_schedules
    print(report_schedules)
    context = {
        'reports': reports,
        'report_schedules':report_schedules
    }
    return HttpResponse(template.render(context, request))

def download_reports(request):
    try:
        filename=f"Dope Deals Report.xlsx"
        global_workbook = Workbook(filename)
        print(request.POST)
        for report_id in request.POST.getlist('download_reports[]'):
            report = Report.objects.get(id=report_id)
            if ReportHistory.objects.filter(report=report)[0] is  None:
                print('running a new report')
                run_report_task(report)
                # global_workbook.sheets[report.short_name]=ReportHistory.objects.filter(report=report).order_by('-id')[0].data
                global_workbook.build_csv_sheet(report.short_name,json.loads(ReportHistory.objects.filter(report=report).order_by('-id')[0].data))
                ReportHistory.objects.filter(report=report).order_by('-id')[0].delete()
            else:
                print('using the existing report')
                # global_workbook.sheets[report.short_name]=ReportHistory.objects.filter(report=report).order_by('-id')[0].data
                global_workbook.build_csv_sheet(report.short_name, json.loads(ReportHistory.objects.filter(report=report).order_by('-id')[0].data))

            print(report)
        global_workbook.write_workbook()
        template = loader.get_template('reports/index.html')
        reports= Report.objects.all().order_by('name')
        # print(reports)
        context = {
            'reports': reports,
        }
        data= open(filename, 'rb')
        os.remove(filename)
        return FileResponse(data)
    except Exception as e:
        messages.error(request, traceback.format_exc())
        return HttpResponseRedirect("/reports/")
    # return HttpResponse(template.render(context, request))

def run_report(request, report_id):
    # print("in run report")
    template = loader.get_template('reports/run_report.html')
    report = Report.objects.get(pk=report_id)
    context= {}
    try:
        # print(len(ReportHistory.objects.filter(report=report)))
        run_report_task(report)
        # print(len(ReportHistory.objects.filter(report=report)))
        context['message']="Report run successfully"
    except Exception as e:
        context['message']=f"Report run failure: {str(e)}"
    return HttpResponse(template.render(context, request))
def getjsreport(request, report_id):
    report = Report.objects.get(pk=report_id)
    response = {}
    try:
        if report.type=='basic':
            if len(ReportHistory.objects.filter(report=report)) == 0:
                run_report_task(report)
                response = build_tabulator_basic_data(json.loads(ReportHistory.objects.filter(report=report).order_by('-id')[0].data))
                ReportHistory.objects.filter(report=report).order_by('-id')[0].delete()
            else:
                response = build_tabulator_basic_data(json.loads(ReportHistory.objects.filter(report=report).order_by('-id')[0].data))
            response = {'message': response, 'status':'success'}
        if report.type=='line':
            if len(ReportHistory.objects.filter(report=report)) == 0:
                run_report_task(report)
                response = build_chartjs_line_data(ReportHistory.objects.filter(report=report))
                ReportHistory.objects.filter(report=report).order_by('-id')[0].delete()
            else:
                response = build_chartjs_line_data(ReportHistory.objects.filter(report=report))
        if report.type=='pie':
            if len(ReportHistory.objects.filter(report=report)) == 0:
                run_report_task(report)
                response = build_chartjs_pie_data(ReportHistory.objects.filter(report=report).order_by('-id')[0])
                ReportHistory.objects.filter(report=report).order_by('-id')[0].delete()
            else:
                response = build_chartjs_pie_data(ReportHistory.objects.filter(report=report).order_by('-id')[0])
        if report.type=='bar':
            if len(ReportHistory.objects.filter(report=report)) ==0:
                run_report_task(report)
                response= build_chartjs_bar_data(ReportHistory.objects.filter(report=report).order_by('-id')[0])
                ReportHistory.objects.filter(report=report).order_by('-id')[0].delete()
            else:
                response= build_chartjs_bar_data(ReportHistory.objects.filter(report=report).order_by('-id')[0])
    except Exception as e:
        # import traceback

        response = { 'response': 'error', 'message': traceback.format_exc()}

    # print(response)

    return JsonResponse(response,content_type='application/javascript')
def getjsreport_history_list(request,report_id):

    data = [['Run Time', 'Action']]
    for rh in ReportHistory.objects.filter(report=Report.objects.get(id=report_id)):
        data.append([rh.creation_date, f'<button class="w3-blue w3-hover-black w3-round"><a href="/reports/{report_id}/view_history/{rh.id}">view</a></button>'])

        # response =
        print(len(data))
    response = {'message': build_tabulator_basic_data(data)}
    print(response['message'][-1])

    return JsonResponse(response, content_type='application/javascript')
def getjsreport_history(request, report_id, history_id):
    report = Report.objects.get(pk=report_id)
    response = {}
    if report.type=='basic':
        response = build_tabulator_basic_data(json.loads(ReportHistory.objects.get(id=history_id).data))
        response = {'response': response}
    if report.type=='line':
        response = build_chartjs_line_data(ReportHistory.objects.get(id=history_id))
    if report.type=='pie':
        response = build_chartjs_pie_data(ReportHistory.objects.get(id=history_id))
    if report.type=='bar':
        response= build_chartjs_bar_data(ReportHistory.objects.get(id=history_id))
    return JsonResponse(response,content_type='application/javascript')
@requires_password_reset
def view_history(request, report_id):
    template = loader.get_template('reports/view_history.html')
    report = Report.objects.get(id=report_id)
    context = {'report_histories': ReportHistory.objects.filter(report=report).order_by('-creation_date'), 'report': report}
    return HttpResponse(template.render(context, request))
    pass
@requires_password_reset
def view_report_history(request, report_id, history_id):
    report = Report.objects.get(id=report_id)
    template = loader.get_template('reports/historical_basic_report.html')
    if report.type=='basic':
        template = loader.get_template('reports/historical_basic_report.html')

    context = {'history': ReportHistory.objects.get(id=history_id), 'report': report}
    return HttpResponse(template.render(context, request))
    pass
@requires_password_reset
def get_report(request, report_id):
    report = Report.objects.get(pk=report_id)
    context = {"request":request, "report":report}
    try:
        if report.type=='basic':
            template = loader.get_template('reports/basic_report.html')
            #get latest run if it exists, if not create it

            # report_history = ReportHistory.objects.filter(report=report).order_by('-id')
            # if len(report_history) == 0:
            #     #need to run one adhoc
            #     run_report_task(report)
            #     report_history = ReportHistory.objects.filter(report=report).order_by('-id')[0]
            #     context['rows'] = json.loads(report_history.data)
            #     context['last_refresh'] = str(datetime.now())
            #     report_history.delete() #cleanup
            #
            # else:
            #     context['rows'] = json.loads(report_history[0].data)
            #     context['last_refresh'] = str(report_history[0].creation_date)
        # latestReportHistory
            print(report.name)
        if report.type=='bar':
            template = loader.get_template('reports/bar_report.html')
        if report.type=='pie':
            template = loader.get_template('reports/pie_report.html')
        if report.type=='line':
            template = loader.get_template('reports/line_report.html')
    except Exception as e:
        print(str(e))
    # if report.type == 'line':

        # context = build_chartjs_line_dataset(ReportHistory.objects.filter(report=report))
    return HttpResponse(template.render(context, request))
    pass
@requires_password_reset
def view_actions(request, report_id):
    template = loader.get_template('reports/view_actions.html')
    report = Report.objects.get(id=report_id)
    context = {'report_actions': ReportAction.objects.filter(report=report).order_by('-creation_date'),
               'report': report}
    return HttpResponse(template.render(context, request))

@requires_password_reset
def view_action_history(request, report_id, action_id):
    template = loader.get_template('reports/view_action_history.html')
    report = Report.objects.get(id=report_id)
    context = {'report_action_histories': ReportActionHistory.objects.filter(report_action=ReportAction.objects.get(id=action_id)).order_by('-creation_date'),
               'report': report}
    return HttpResponse(template.render(context, request))
@requires_password_reset
def view_action_result(request, report_id, history_id):
    template = loader.get_template('reports/view_action_result.html')
    report = Report.objects.get(id=report_id)
    context = {'action_result': ReportActionHistory.objects.get(id=history_id),
               'report': report}
    return HttpResponse(template.render(context, request))

def create_report_history(request, report_id):
    # =
    # print(request.body)
    response = {}
    # _vulnerability = Vulnerability.objects.get(index=vulnerability)
    try:
        import django.db
        django.db.close_old_connections()
        report = Report.objects.get(id=report_id)
        json_data = json.loads(request.body)
        # print(json_data)
        history = ReportHistory()
        history.report = report
        history.data = json.dumps(json_data)
        history.creation_date = timezone.now()
        django.db.close_old_connections()
        history.save()
        print(f"saved report_history for report: {report.name}")
        response['status'] = 'success'
        response['message'] = 'success'
    except Exception as e:
        traceback.print_exc()
        response['status'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response, content_type='application/javascript')



    # return HttpResponse("Hello")