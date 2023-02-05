# password_reset_events = PasswordResetEvent.objects.filter(user=request.user).order_by('-last_password_reset')
# if len(password_reset_events) > 0:
#     latest_event = password_reset_events[0]
#     if (now() - latest_event.last_password_reset).days < 365:
#         messages.error(request, "You are not eligible for a password reset at this time")
#         return HttpResponseRedirect("/")
from django.contrib import messages
from django.urls import reverse
from django.utils.timezone import now

from functools import wraps
from django.http import HttpResponseRedirect

from config.models import PasswordResetEvent


def requires_password_reset(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return function(request, *args, **kwargs)
        password_reset_events = PasswordResetEvent.objects.filter(user=request.user).order_by('-last_password_reset')
        if len(password_reset_events) > 0:
            latest_event = password_reset_events[0]
            if (now() - latest_event.last_password_reset).days < 365:
                # messages.error(request, "You are not eligible for a password reset at this time")
                return function(request, *args, **kwargs)
            else:
                messages.error(request, "You must reset your password every 365 days")
                return HttpResponseRedirect(reverse("password_reset"))
        else:
            messages.error(request, "You must reset your password to proceed")
            return HttpResponseRedirect(reverse("password_reset"))

    return wrap
