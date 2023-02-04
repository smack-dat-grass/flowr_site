import traceback

from django.http import HttpResponse, JsonResponse
from django.template import loader

from alerts.models import HealthCheck,HealthCheckMetric
from .functions import build_health_check_graph

def health_checks(request):
    metrics = []
    template = loader.get_template('alerts/health_checks.html')
    for health_check in HealthCheck.objects.all():
        if len(HealthCheckMetric.objects.filter(health_check=health_check)) > 0:
            metrics.append(HealthCheckMetric.objects.filter(health_check=health_check).order_by('-creation_date')[0])
    return HttpResponse(template.render({"health_checks":metrics},request))
def show_headers(request):
    metrics = []
    template = loader.get_template('alerts/show_headers.html')
    results = {}
    for k,v in request.META.items():
        results[k]=v
    for k,v in request.headers.items():
        if k not in results:
            results[k]=v
    return HttpResponse(template.render({"headers":results},request))

def get_historical_graph(request, health_check_id,days=1):
    # tool = Tool.objects.get(id=tool_id)
    response = {}
    try:
        response['message'] = build_health_check_graph(HealthCheck.objects.get(id=health_check_id),days)
        response['status'] = 'success'
    except Exception as e:
        traceback.print_exc()
        response['status'] = 'error'
        response['message'] = str(e)

    # response['status'] = 'success'
    # response['message'] = 'valid'

    return JsonResponse(response, content_type='application/javascript')
def historical_graph(request, health_check_id,days=1):
    metrics = []
    template = loader.get_template('alerts/health_check_graph.html')
    # for health_check in HealthCheck.objects.all():
    #     if len(HealthCheckMetric.objects.filter(health_check=health_check)) > 0:
    #         metrics.append(HealthCheckMetric.objects.filter(health_check=health_check).order_by('-creation_date')[0])
    health_check = HealthCheck.objects.get(id=health_check_id)
    return HttpResponse(template.render({"health_check":health_check, "days":days}, request))