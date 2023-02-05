# attributes = json.loads(report.attributes)
from django.utils import timezone
from datetime import datetime
from config.classes import OracleConnector
from config.models import  Connection

attributes = json.loads(report.attributes)
rh = ReportHistory.objects.filter(report=report).order_by('-creation_date')[0]
report_history = json.loads(rh.data)
ora_conn = OracleConnector(Connection.objects.get(name=report.connection.name))
ora_conn.open_connection()
# inactive_offenders = []
# for i in range(1, len(report_history)):
#     if report_history[i][7].lower() == 'i':  # inactive FNSSO check
#         inactive_offenders.append(report_history[i])

#first, we need to identify the inactive fnssos that have pending requests
try:

        ora_conn.execute_update(attributes['remediation_sql'])
        create_notification(f"{report.name}", f"{len(report_history)-1} {attributes['remediation_message']} See <a href='/reports/{report.id}/get'>the report</a> for full details",minutes=15)
        # ora_conn.commit()
        # ora_conn.close_connection()
        # create_notification(f"{report.name}",f"{len(inactive_offenders)} pending requests for inactive FNSSOs were cancelled.These records will drop off the report after the next refresh. See <a href='/reports/{report.id}/get'>the report</a> for full details", minutes=15)
    #
    # if (len(report_history)-1)-len(inactive_offenders) > attributes['threshold']:
    #     create_alert(f'{report.name}', f"Pending FNSSO requests in InfraIDM exceeds {attributes['threshold']}. The current backlog count is {(len(report_history)-1)-len(inactive_offenders)}.<br><br>Please investigate, see <a href='/reports/{report.id}/get'>the report</a> for details")
except Exception as e:
    ora_conn.close_connection()
    create_alert(f'{report.name}',f"Dope Deals was unable to run the remediation sql for {report.name} as a result of the following error: {str(e)}. This may require manual intervention")
