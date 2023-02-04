from django.contrib import admin
from .models import Connection, Credential, Configuration,NavigationLink,PasswordResetEvent
# Register your models here.
admin.site.register(Connection)
admin.site.register(Credential)
admin.site.register(Configuration)
admin.site.register(NavigationLink)
admin.site.register(PasswordResetEvent)
