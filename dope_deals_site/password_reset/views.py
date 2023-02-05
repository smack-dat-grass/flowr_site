from datetime import datetime

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from config.models import PasswordResetEvent
from django.utils.timezone import now


@login_required(login_url='/accounts/login')
def password_reset(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            password_event = PasswordResetEvent()
            password_event.user = request.user
            password_event.save()
            return HttpResponseRedirect("/")
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dope_deals_site/password_reset.html', {
        'form': form
    })