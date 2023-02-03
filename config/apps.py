from django.apps import AppConfig

from health_check.plugins import plugin_dir

class ConfigConfig(AppConfig):
    # name = 'healthcheckconfig'
    name='config'
    def ready(self):
        from .backends import UsersLoggedInTodayHealthCheckBackend
        plugin_dir.register(UsersLoggedInTodayHealthCheckBackend)
        print('registered healthcheckss')



# from .backends import UsersLoggedInTodayHealthCheckBackend
# class MyAppConfig(AppConfig):
#     name = 'my_app'

