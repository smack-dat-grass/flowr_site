from django.urls import path

from . import views
from .health_checks.views import get_historical_graph,health_checks,historical_graph,show_headers
urlpatterns = [
    path('', views.index, name='index'),
    path('health_checks/', health_checks, name='health_checks'),
    path('get_past_alerts/', views.get_past_alerts, name='get_past_alerts'),
    path('show_headers/', show_headers, name='show_headers'),
    path('health_checks/<int:health_check_id>/historical_graph/<int:days>/', historical_graph, name='historical_graph'),
    # path('health_checks/<int:health_check_id>/get_historical_graph', get_historical_graph, name='get_historical_graph'),
    path('health_checks/<int:health_check_id>/get_historical_graph/<int:days>/', get_historical_graph, name='get_historical_graph'),
    path('<int:alert_id>/resolve', views.resolve, name='resolve'),
    path('<int:alert_id>/submit_resolution', views.submit_resolution, name='submit_resolution'),

]