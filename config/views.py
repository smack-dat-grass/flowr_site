from django.http import JsonResponse
from django.shortcuts import render
from .models import Connection
from django.conf import settings
from .functions import test_connection as _test_connection, close_connection as _close_connection, open_connection as _open_connection
from dope_deals_site.decorators import requires_password_reset
# Create your views here.
def index(request):
    pass
@requires_password_reset
def connections(request):
    context= {"connections":Connection.objects.all().order_by("name")}
    active_connections = {}
    for k in settings.DATABASE_POOL.keys():
        active_connections[k]={}
        active_connections[k]["timeout"]=settings.DATABASE_POOL[k]['timeout']
        active_connections[k]["created"]=settings.DATABASE_POOL[k]['created']
        active_connections[k]["connection"]=Connection.objects.get(name=k)
    context['active_connections']=active_connections
    print(active_connections)
    return render(request, "config/connections.html", context)
    pass
def test_connection(request, connection_id):
    connection =Connection.objects.get(id=connection_id)
    response ={}
    try:
        _test_connection(connection)
        response['status']='success'
        response['message']=f'Connection to {connection.name} successful'

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
    return JsonResponse(response,content_type='application/javascript')
def open_connection(request, connection_id):
    connection = Connection.objects.get(id=connection_id)
    response = {}
    try:
        _open_connection(connection)
        response['status'] = 'success'
        response['message'] = f'Connection to {connection.name} opened successfully'

    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
    return JsonResponse(response, content_type='application/javascript')

def close_connection(request, connection_id):
    connection = Connection.objects.get(id=connection_id)
    response = {}
    try:
        _close_connection(connection)
        response['status'] = 'success'
        response['message'] = f'Connection to {connection.name} closed successfully'

    except Exception as e:
        import traceback
        traceback.print_exc()
        response['status'] = 'error'
        response['message'] = str(e)
    return JsonResponse(response, content_type='application/javascript')
