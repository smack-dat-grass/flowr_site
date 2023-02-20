from django.db import models

# Create your models here.
from .classes import StrainType
from django.utils.timezone import now
class StrainSource(models.Model):
    name =models.CharField(max_length=100, null=False)
    url =models.TextField(null=True, blank=True)
class TerpeneAroma(models.Model):
    name = models.CharField(max_length=200, null=False )
    description = models.TextField(null=True, blank=True)
class TerpeneEffect(models.Model):
    name = models.CharField(max_length=200, null=False )
    description = models.TextField(null=True, blank=True)

class Terpene(models.Model):
    name = models.CharField(max_length=200, null=False,)
    description = models.TextField(null=True, blank=True)
    aroma = models.ManyToManyField(TerpeneAroma)
    effects = models.ManyToManyField(TerpeneEffect)
class Strain(models.Model):

    def __str__(self):
        return self.name
    #todo add scheduling piece
    name = models.CharField(max_length=100, null=False)
    type  = models.CharField(choices=((StrainType.INDICA, StrainType.INDICA), (StrainType.SATIVA,StrainType.SATIVA), (StrainType.HYBRID, StrainType.HYBRID)),default=StrainType.HYBRID, max_length=150)
    description = models.TextField(null=True, blank=True)
    source=models.ForeignKey(StrainSource,on_delete=models.RESTRICT, null=False)
    image = models.TextField(null=True, blank=True)
    aliases = models.TextField(null=True, blank=True)
    parents = models.ManyToManyField("self", null=True,blank=True)
    children = models.ManyToManyField("self", null=True,blank=True)
    terpenes = models.ManyToManyField(Terpene, null=True,blank=True)
    creation_date = models.DateTimeField(null=False, default=now)
    # resolution_date = models.DateTimeField(null=True, blank=True)