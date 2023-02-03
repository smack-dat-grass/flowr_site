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
    help = 'Export objects from the Database'
    object_types= {"Task":Task, 'ReportTrigger':ReportTrigger, 'ReportAction':ReportAction,'HealthCheck':HealthCheck,'Report':Report,'ObjectType':ObjectType, 'SearchSource':SearchSource}
    config_keys=['name', 'description', 'attributes','code']
    def process_object(self, object):
        pass
    def validate_config(self, config, config_name):
        for key in self.config_keys:
            if key not in config:
                raise Exception(f"Bad config file, missing '{key}' in {config_name}")

    def update_object(self, object, config):
        object.name=config['name']
        object.description=config['description']
        with open(config['code']) as f:
            object.code=f.read()
        with open(config['attributes']) as f:
            json_data = json.loads(f.read())
            object.attributes = json.dumps(json_data)
        object.save()
    def handle(self, *args, **kwargs):
        for object_type in self.object_types.keys():
            print(f"Processing {object_type} objects")
            object_path =f"{settings.BASE_DIR}/objects/{object_type}"
            if not os.path.exists(object_path):
                os.mkdir(object_path)
            if object_type!='ObjectType':
                for object in self.object_types[object_type].objects.all():
                    #start loading data
                    print(f"Processing {object.name} {object_type}")
                    attrs = json.loads(object.attributes)
                    config = {"name":object.name, "description": object.description, "attributes":"attributes.json"}
                    # code = task.code
                    if object_type=='SearchSource':
                        export_path = f"{settings.BASE_DIR}/objects/{object_type}/{object.name.replace(' ', '').replace('/', '')}_{object.object_type.name.replace(' ', '').replace('/', '')}"
                    else:
                        export_path = f"{settings.BASE_DIR}/objects/{object_type}/{object.name.replace(' ', '').replace('/', '')}"
                    if not os.path.exists(export_path):
                        os.mkdir(export_path)
                    #write attrs first
                    with open(f"{export_path}/{config['attributes']}", "w") as f:
                        f.write(json.dumps(attrs))
                    if object_type in ['HealthCheck', 'ReportAction', 'Task', 'ReportTrigger', 'Report', 'SearchSource']:
                        code = object.code
                        if os.path.exists(f"{export_path}/configuration.json"):
                            with open(f"{export_path}/configuration.json", "r") as f: #use existing filename for code where applicable
                                _config = json.loads(f.read())
                                config['code'] = _config['code']
                        if object_type=='SearchSource':
                            config['object_type']=object.object_type.name
                            config['code']='main.sql'
                            #read in filename
                        else:
                            if object_type in ['HealthCheck', 'ReportAction', 'Task', 'ReportTrigger']:
                                config['code'] = 'main.py'
                            else: #this just leaves reports and search sorces
                                if object.connection is None: #assuming no connection
                                    config['code'] = 'main.sql'
                                else:
                                    if object.connection.type ==API_CONNECTOR_TYPE:
                                        config['code'] = 'main.py'
                                    elif object.connection.type == LDAP_CONNECTOR_TYPE:
                                        config['code'] = 'main.ldiff'
                                    else:
                                        config['code'] = 'main.sql'
                        #now we can write the code piece
                        with open(f"{export_path}/{config['code']}", "w") as f:
                            f.write(code)
                        with open(f"{export_path}/configuration.json", "w") as f:
                            f.write(json.dumps(config))
                            print(f"Wrote config for {object.name}: {config}")
            else:# now we just need to process the object types
                for object in self.object_types[object_type].objects.all():
                    # start loading data
                    # attrs = json.loads(object.attributes)
                    config = {"name": object.name, "description": object.description}
                    # code = task.code
                    export_path = f"{settings.BASE_DIR}/objects/{object_type}/{object.name.replace(' ', '').replace('/', '')}"
                    if not os.path.exists(export_path):
                        os.mkdir(export_path)
                    # write attrs first
                    with open(f"{export_path}/configuration.json", "w") as f:
                        f.write(json.dumps(config))
                        print(f"Wrote config for {object.name}: {config}")

                        #
                            # with open(f"{export_path}/{config['code']}", "w") as f:
                            #     f.write(json.dumps(attrs))




                # for object_config in os.listdir(object_path):
                #     os.chdir(f"{object_path}/{object_config}")
                #     with open("configuration.json") as f:
                #         config = json.loads(f.read())
                #         print(config, object_config)
                #         self.validate_config(config, object_config)
                #         if object_type=='Task': #handle task loading
                #             if len([x for x in Task.objects.filter(name=config['name'])]) > 0:
                #
                #                 task = Task.objects.get(name=config['name'])
                #                 self.update_object(task,config)
                #             else:
                #                 self.update_object(Task(), config)
                #         if object_type == 'ReportTrigger':  # handle task loading
                #             if len([x for x in ReportTrigger.objects.filter(name=config['name'])]) > 0:
                #
                #                 trigger = ReportTrigger.objects.get(name=config['name'])
                #                 self.update_object(trigger, config)
                #             else:
                #                 self.update_object(ReportTrigger(), config)
                #         if object_type == 'ReportAction':  # handle task loading
                #             if len([x for x in ReportAction.objects.filter(name=config['name'])]) > 0:
                #
                #                 action = ReportAction.objects.get(name=config['name'])
                #                 self.update_object(action, config)
                #             else:
                #                 self.update_object(ReportAction(), config)
                #         if object_type == 'HealthCheck':  # handle task loading
                #             if len([x for x in HealthCheck.objects.filter(name=config['name'])]) > 0:
                #
                #                 health_check = HealthCheck.objects.get(name=config['name'])
                #                 self.update_object(health_check, config)
                #             else:
                #                 self.update_object(HealthCheck(), config)
                #         if object_type == 'Report':  # handle task loading
                #             if len([x for x in Report.objects.filter(name=config['name'])]) > 0:
                #
                #                 action = Report.objects.get(name=config['name'])
                #                 self.update_object(action, config)
                #             else:
                #                 self.update_object(Report(), config)
                            # self.process_object()

        time = timezone.now().strftime('%X')

        # self.stdout.write("It's now %s" % time)