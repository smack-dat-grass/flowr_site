from datetime import timedelta

from django.http import HttpResponse
from django.utils import timezone
from health_check.backends import BaseHealthCheckBackend
from django.contrib.auth.models import User
class UsersLoggedInTodayHealthCheckBackend(BaseHealthCheckBackend):
    #: The status endpoints will respond with a 200 status code
    #: even if the check errors.
    critical_service = True

    def check_status(self):
        # The test code goes here.
        # You can use `self.add_error` or
        # raise a `HealthCheckException`,
        # similar to Django's form validation.
        # self.
        try:
            [x for x in User.objects.filter(last_login__gt=timezone.now()-timedelta(days=1))]
        except Exception as e:
            self.add_error(e,e)



    def identifier(self):
        return self.__class__.__name__  # Display name on the endpoint.