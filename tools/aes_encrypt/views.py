from django.http import JsonResponse, HttpResponse
from django.template import loader

from tools.models import Tool
from .functions import aes_decrypt as _decrypt,aes_encrypt as _encrypt

def aes_encrypt(request, tool_id):
    tool = Tool.objects.get(id=tool_id)
    template = loader.get_template("tools/aes_encrypt/index.html")
    context = {'tool': tool}
    # context['data'] = load_orphaned_fnssos(request, tool)
    return HttpResponse(template.render(context, request))
def encrypt(request, tool_id, key, value):
    tool = Tool.objects.get(id=tool_id)
    response = {}
    try:

        value  = _encrypt(key, value)
        response['message'] = value
        response['response'] = 'success'

    except Exception as e:
        print("in catch")
        response['response'] = 'error'
        response['message'] = str(e)

    return JsonResponse(response, content_type='application/javascript')

def decrypt(request, tool_id, key, value):
    # tool = Tool.objects.get(id=tool_id)
    response = {}
    try:
        value = _decrypt(key, value)
        response['message'] =  value
        response['response'] = 'success'

    except Exception as e:
        print("in catch")
        response['response'] = 'error'
        response['message'] = str(e)
    print(response)
    return JsonResponse(response, content_type='application/javascript')