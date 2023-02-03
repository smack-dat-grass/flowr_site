from django.contrib import messages

from .models import NavigationLink

from functools import wraps
from django.http import HttpResponseRedirect, JsonResponse


def can_access_url(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        for link in NavigationLink.objects.all():
            if link.location in request.path and (
                    link.group is not None and not request.user.groups.filter(name=link.group).exists()):
                messages.info(request, f"You do not have permission to view {request.path}", )
                return HttpResponseRedirect('/')

        return function(request, *args, **kwargs)

    return wrap





def can_access_url_api(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        for link in NavigationLink.objects.all():
            if link.location in request.path and (
                    link.group is not None and not request.user.groups.filter(name=link.group).exists()):
                # messages.info(request, ", )
                return JsonResponse({"status":"error","reponse":"error","message":f"You do not have permission to view {request.path}"})

        return function(request, *args, **kwargs)

    return wrap
