from django.core.management.base import BaseCommand
from django.utils import timezone
from config.models import CodeModel, ORACLE_CONNECTOR_TYPE, MYSQL_CONNECTOR_TYPE,LDAP_CONNECTOR_TYPE,POSTGRE_CONNECTOR_TYPE,API_CONNECTOR_TYPE
from tasks.models import Task
from reports.models import ReportTrigger, ReportAction,Report
from alerts.models import HealthCheck
from search.models import ObjectType, SearchSource
import os,json
from django.conf import settings
class Command(BaseCommand):
    help = 'Load objects into the Database'
    object_types= {"Task":Task, 'ReportTrigger':ReportTrigger, 'ReportAction':ReportAction,'HealthCheck':HealthCheck,'Report':Report,'ObjectType':ObjectType, 'SearchSource':SearchSource}
    config_keys=['name', 'description', 'attributes','code']
    def process_object(self, object):
        pass
    def validate_config(self, config, config_name):
        for key in self.config_keys:
            if key not in config:
                raise Exception(f"Bad config file, missing '{key}' in {config_name}")

    def update_object(self, _object, config):
        _object.name=config['name']
        _object.description=config['description']
        if 'criticality' in config:
            _object.criticality = config['criticality']
        if type(_object) == SearchSource:
            _object.object_type = ObjectType.objects.get(name=config['object_type'])
        with open(config['code']) as f:
            _object.code=f.read()
        with open(config['attributes']) as f:
            json_data = json.loads(f.read())
            _object.attributes = json.dumps(json_data)
        _object.save()
    def handle(self, *args, **kwargs):
        for object_type in self.object_types.keys():
            print(f"Processing {object_type} objects")
            object_path =f"{settings.BASE_DIR}/objects/{object_type}"
            if os.path.exists(object_path):
                for object_config in os.listdir(object_path):
                    os.chdir(f"{object_path}/{object_config}")
                    if object_type=='ObjectType':
                        with open("configuration.json") as f:
                            config = json.loads(f.read())
                        print(config, object_config)
                        if len([x for x in ObjectType.objects.filter(name=config['name'])]) > 0:

                            ot = ObjectType.objects.get(name=config['name'])

                            # self.update_object(object, config)
                        else:
                            ot = ObjectType()
                        ot.name= config['name']
                        ot.description= config['description']
                        ot.save()
                            # self.update_object(self.object_types[object_type](), config)
                    else:
                        with open("configuration.json") as f:
                            config = json.loads(f.read())
                        print(config, object_config)
                        self.validate_config(config, object_config)
                        if len([x for x in self.object_types[object_type].objects.filter(name=config['name'])]) > 0:

                            if object_type=='SearchSource':
                                object = self.object_types[object_type].objects.get(name=config['name'], object_type__name=config['object_type'])
                            else:
                                object = self.object_types[object_type].objects.get(name=config['name'])
                            self.update_object(object, config)
                        else:
                            # if object_type=='SearchSource':
                            #     _obj = self.object_types[object_type]()
                            #     self.update_object(_obj, config)
                            # else:
                            self.update_object(self.object_types[object_type](), config)

                    # with open("configuration.json") as f:
                    #     config = json.loads(f.read())
                    #     print(config, object_config)
                    #     self.validate_config(config, object_config)
                    #     if object_type=='Task': #handle task loading
                    #         if len([x for x in Task.objects.filter(name=config['name'])]) > 0:
                    #
                    #             task = Task.objects.get(name=config['name'])
                    #             self.update_object(task,config)
                    #         else:
                    #             self.update_object(Task(), config)
                    #     if object_type == 'ReportTrigger':  # handle task loading
                    #         if len([x for x in ReportTrigger.objects.filter(name=config['name'])]) > 0:
                    #
                    #             trigger = ReportTrigger.objects.get(name=config['name'])
                    #             self.update_object(trigger, config)
                    #         else:
                    #             self.update_object(ReportTrigger(), config)
                    #     if object_type == 'ReportAction':  # handle task loading
                    #         if len([x for x in ReportAction.objects.filter(name=config['name'])]) > 0:
                    #
                    #             action = ReportAction.objects.get(name=config['name'])
                    #             self.update_object(action, config)
                    #         else:
                    #             self.update_object(ReportAction(), config)
                    #     if object_type == 'HealthCheck':  # handle task loading
                    #         if len([x for x in HealthCheck.objects.filter(name=config['name'])]) > 0:
                    #
                    #             health_check = HealthCheck.objects.get(name=config['name'])
                    #             self.update_object(health_check, config)
                    #         else:
                    #             self.update_object(HealthCheck(), config)
                    #     if object_type == 'Report':  # handle task loading
                    #         if len([x for x in Report.objects.filter(name=config['name'])]) > 0:
                    #
                    #             action = Report.objects.get(name=config['name'])
                    #             self.update_object(action, config)
                    #         else:
                    #             self.update_object(Report(), config)
                            # self.process_object()

        time = timezone.now().strftime('%X')

        # self.stdout.write("It's now %s" % time)