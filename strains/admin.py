from django.contrib import admin
from .models import Terpene,TerpeneEffect,TerpeneAroma,StrainSource,Strain
# Register your models here.
admin.site.register(Strain)
admin.site.register(Terpene)
admin.site.register(TerpeneEffect)
admin.site.register(TerpeneAroma)
admin.site.register(StrainSource)