from django.shortcuts import render
from django.template import loader
from .models import  Alert, HealthCheck, HealthCheckMetric
# Create your views here.
from django.utils.timezone import now
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from config.decorators import can_access_url
from dope_deals_site.decorators import requires_password_reset
from django.contrib.auth.decorators import login_required
from reports.functions import build_tabulator_basic_data
@login_required(login_url='/accounts/login')
@can_access_url
@requires_password_reset
def index(request):
    template = loader.get_template('alerts/index.html')
    return HttpResponse(template.render(
        {"active_alerts": Alert.objects.filter(active=True).order_by('-creation_date'), "inactive_alerts":Alert.objects.filter(active=False).order_by('-resolution_date')[:250]},
        request))
@login_required(login_url='/accounts/login')
@can_access_url
@requires_password_reset
def resolve(request, alert_id):
    template = loader.get_template('alerts/resolve.html')

    return HttpResponse(template.render(
        {"alert": Alert.objects.get(id=alert_id)},
        request))
@login_required(login_url='/accounts/login')
@can_access_url
@requires_password_reset
def submit_resolution(request, alert_id):
    if 'resolution' not in request.POST:
        print('wtf')
        return HttpResponseRedirect(f"/alerts/{alert_id}/resolve")
    else:
        alert= Alert.objects.get(id=alert_id)
        alert.resolution=request.POST['resolution']
        alert.active=False
        alert.resolution_date = now()
        alert.save()
        messages.info(request,f"{alert.name} resolved")
        return HttpResponseRedirect(f"/alerts/")
@login_required(login_url='/accounts/login')
@can_access_url
@requires_password_reset
def get_past_alerts(request):
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