from datetime import datetime
class DjangoSiteHealth:
    object_type =''
    name = ''
    last_updated= datetime.now()
    delta=None
    schedule=''
    criticality=5
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'schedule' in kwargs:
            self.name = kwargs['schedule']
        if 'object_type' in kwargs:
            self.name = kwargs['object_type']
        if 'last_updated' in kwargs:
            self.last_updated=kwargs['last_updated']
        if 'delta' in kwargs:
            self.delta = kwargs['delta']
        if 'criticality' in kwargs:
            self.criticality = kwargs['criticality']
            # self.criticality = kwargs['criticality']
    def __str__(self):
        return f"Name: {self.name} Type: {self.object_type} Last Updated: {self.last_updated} Delta: {self.delta} Schedule: {self.schedule}"