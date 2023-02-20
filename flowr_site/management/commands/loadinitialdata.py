from django.core.management.base import BaseCommand
from django.utils import timezone
# from config.models import CodeModel, ORACLE_CONNECTOR_TYPE, MYSQL_CONNECTOR_TYPE,LDAP_CONNECTOR_TYPE,POSTGRE_CONNECTOR_TYPE,API_CONNECTOR_TYPE
# from tasks.models import Task
# from reports.models import ReportTrigger, ReportAction,Report
# from alerts.models import HealthCheck
# from search.models import ObjectType, SearchSource
from locations.models import Location, City, State
from django.conf import settings
import os,json
from django.conf import settings
class Command(BaseCommand):
    help = 'Load objects into the Database'
    object_types = [State(),City()]
    # object_types= {"Task":Task, 'ReportTrigger':ReportTrigger, 'ReportAction':ReportAction,'HealthCheck':HealthCheck,'Report':Report,'ObjectType':ObjectType, 'SearchSource':SearchSource}
    # config_keys=['name', 'description', 'attributes','code']
    def load_object_type_json(self, _object):
        print(f"Loading {_object.__class__.__name__} data")
        with open(f"{settings.BASE_DIR}/initial_data/{_object.__class__.__name__}.json", "r") as f:
            return json.loads(f.read())

    def process_json(self,data_json, _object):
        objects = []
        if isinstance(_object, City):
            for unique_key, data in data_json.items():
                if len([x for x in City.objects.filter(name=data['name'], state=State.objects.get(code=data['state']))]) ==0:
                    city = City()
                    city.state=State.objects.get(code=data['state'])
                    city.name=data['name']
                    city.save()
                    print(f"Loaded {city.name}, {city.state.code}")

        elif isinstance(_object, State):
            for name, data in data_json.items():
                if len([x for x in State.objects.filter(name=name)])==0:
                    state=  State()
                    state.name=name
                    state.code=data['code']
                    state.legal=data['legal']
                    state.save()
                    print(f"Loaded {state.name}")


    def handle(self, *args, **kwargs):
        for object_type in self.object_types:
            print(f"Loading data for {object_type.__class__.__name__}")
            self.process_json(self.load_object_type_json(object_type),object_type)
