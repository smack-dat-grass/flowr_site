import json
from config.classes import OracleConnector
from config.models import  Connection
import xmltodict
required_configs = ['threshold', 'alert_message']
report_history = json.loads(ReportHistory.objects.filter(report=report).order_by('-creation_date')[0].data)
attributes = json.loads(report.attributes)
valid = True
for config in required_configs:
    if config not in attributes.keys():
        create_alert(report.name, f"An alert was triggered but could not be created. Missing {config}")
        valid=False

if valid:
    create_alert(report.name, f"<br>Threshold: {attributes['threshold']} Current Value: {len(report_history)}<br> {attributes['alert_message']}<br><br> For details, click <a href='/reports/{report.id}/get'>here</a>")





