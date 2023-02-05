# from .functions import run_search as rs
import urllib.parse, traceback
from config.decorators import can_access_url
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import Tool
from django.urls import reverse
# from datetime import  datetime
from django.template import loader
from django.contrib import messages
from dope_deals_site.decorators import requires_password_reset




@requires_password_reset
@can_access_url
def index(request):
    template = loader.get_template('tools/index.html')
    context = {'tools':Tool.objects.all().order_by('name')}
    return HttpResponse(template.render(context, request))
@requires_password_reset
@can_access_url
def tool(request, tool_id):
    tool = Tool.objects.get(id=tool_id)
    # template = loader.get_template(tool.template)
    return HttpResponseRedirect(reverse(tool.url, args=[tool_id]))
    # context = {'tool': tool}
    # return HttpResponseRedirect(template.render(context, request))

