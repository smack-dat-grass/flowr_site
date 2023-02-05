from django.contrib import admin
from locations.models import City, State, Location
# Register your models here.
admin.site.register(City)
admin.site.register(State)
admin.site.register(Location)
