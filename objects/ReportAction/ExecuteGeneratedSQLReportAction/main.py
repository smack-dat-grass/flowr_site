from config.classes import OracleConnector
from config.models import  Connection
attributes = json.loads(report.action.attributes)
report_attributes = json.loads(report.attributes)
if "index" in report_attributes:
    rh = ReportHistory.objects.filter(report=report).order_by('-creation_date')[0]
    report_history = json.loads(rh.data)
    lines = []


    ora_conn = OracleConnector(Connection.objects.get(name=report.connection.name))
    ora_conn.open_connection()
    for i in range(1, len(report_history)):
        lines.append(report_history[i][0])
        ora_conn.execute_update(report_history[i][-1])

    report_action_history.attributes = json.dumps({"updated_records":len(lines), "message": "Updated records will drop off of the report on the next refresh"})
    report_action_history.save()
    ora_conn.close_connection()

    create_notification(f"{report.name} Action Taken", f"{len(lines)} statements executed", hours=1)
else:
    create_alert(f"{report.name} could not be actioned, 'index' report attribute is missing. Please specify a column index and try again")