from django.db import models
from config.models import Connection

# Create your models here.
class Tool(models.Model):
    name=models.CharField(max_length=200, null=False)
    description=models.TextField(null=False)
    connection=models.ForeignKey(Connection, models.CASCADE)
    groups=models.ManyToManyField("auth.Group",null=True,blank=True)
    url=models.CharField(max_length=500,null=False, default="url", help_text="The named url entrypoint")
    attributes=models.TextField(null=False, default={})

    def __str__(self):
        return self.name
