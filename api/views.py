from django.shortcuts import render

# Create your views here.
# @login_required(login_url='/accounts/login')
# @can_access_url
# @requires_password_reset
from django.shortcuts import render
from django.template import loader
# Create your views here.
from django.utils.timezone import now
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
# from config.decorators import can_access_url
# from dope_deals_site.decorators import requires_password_reset
# from django.contrib.auth.decorators import login_required
# from reports.functions import build_tabulator_basic_data
def index(request):
    pass
def query_without_keywords(request, city, state,type,price_limit, thc_limit):
    # report = Report.objects.get(pk=report_id)
    response = {}

    data = [['Creation Date','Name','Resolution','Resolution Date','Description']]
    for alert in Alert.objects.filter(active=False).exclude(resolution_date__isnull=True).order_by('-resolution_date'):
        data.append([ alert.creation_date,alert.name,alert.resolution,alert.resolution_date,alert.description[:250]])

    # response =
    print(len(data))
    response = {'message': build_tabulator_basic_data(data)}
    print(response['message'][-1])

    return JsonResponse(response,content_type='application/javascript')
def query_with_keywords(request, city, state,type,price_limit, thc_limit,keywords):
    # report = Report.objects.get(pk=report_id)
    response = {}

    data = [['Creation Date','Name','Resolution','Resolution Date','Description']]
    for alert in Alert.objects.filter(active=False).exclude(resolution_date__isnull=True).order_by('-resolution_date'):
        data.append([ alert.creation_date,alert.name,alert.resolution,alert.resolution_date,alert.description[:250]])

    # response =
    print(len(data))
    response = {'message': build_tabulator_basic_data(data)}
    print(response['message'][-1])

    return JsonResponse(response,content_type='application/javascript')