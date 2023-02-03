clear_alerts(report.name)
attributes  = json.loads(report.attributes)
if record_count_greater_than(report, attributes['threshold']):
    action_report(report)