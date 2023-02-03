from django.contrib import admin
from .models import Connection, Credential, Configuration,NavigationLink,GEBusinessGroup,GEBusiness, PasswordResetEvent
# Register your models here.
admin.site.register(Connection)
admin.site.register(Credential)
admin.site.register(Configuration)
admin.site.register(NavigationLink)
admin.site.register(GEBusiness)
admin.site.register(GEBusinessGroup)
admin.site.register(PasswordResetEvent)
