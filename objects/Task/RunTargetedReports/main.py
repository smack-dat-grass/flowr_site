from reports.functions import run_report
# run_targeted_reports(task_name, task_result)
task_attrs = json.loads(task.attributes)
for report_id in task_attrs['reports']:
    run_report(Report.objects.get(id=report_id))
    # import django.db
    # django.db.close_old_connections()
    check_report_trigger(Report.objects.get(id=report_id))
    print(f"Completed run of {report_id}")
    print(f"Ran: {Report.objects.get(id=report_id).name}")