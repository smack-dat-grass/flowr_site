from django.db import models

# Create your models here.
from django.utils.timezone import now

# from config.models import Connection
from config.models import Connection,CodeModel

class ObjectType(models.Model):
    name=models.CharField(max_length=100, null=False, blank=True, default="Please add a name")
    description=models.TextField(null=False, default="Please add a description")
    creation_date = models.DateTimeField(null=False, default=now())
    group = models.ForeignKey("auth.Group", null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}: {self.description}"
    pass

class SearchSource(CodeModel):
    # name = models.CharField(max_length=100, null=False, blank=True, default="Please add a name")
    # description = models.TextField(null=False, default="Please add a description")
    # creation_date = models.DateTimeField(null=False, default=now())
    connection = models.ForeignKey(Connection, null=True, on_delete=models.CASCADE)
    # search_query = models.TextField(null=False)
    group = models.ForeignKey("auth.Group", null=True, blank=True, on_delete=models.CASCADE)
    object_type=models.ForeignKey(ObjectType, null=True, on_delete=models.CASCADE)
    # attributes = models.TextField(null=False, default='{}', help_text='json attributes')
    def __str__(self):
        return f"{self.object_type.name}: {self.name}"