if len(report_history) > 1:
    print("passed the test")
    report_action_history.attributes=json.dumps({"status":"Success"})
    report_action_history.save()