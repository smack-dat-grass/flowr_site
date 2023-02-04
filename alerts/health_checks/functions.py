import numpy
from django.utils import timezone
from reports.functions import random_color
from alerts.models import HealthCheckMetric

def build_health_check_graph(health_check,days):
    history = HealthCheckMetric.objects.filter(health_check=health_check).order_by('-creation_date')
    print(f"pulling data for {days} days")
    print(f"found {len(history)} report histories")
    health_checks =[history[0]]#preload with latest record
    # print(health_checks[0].creation_date)
    last_index = 0
    for i in range(1,len(history)): #should be in desc order
        # print(f"Processing metric from {history[i].creation_date}\nLast Processed Metric From: {history[last_index]}\nDelta:{(history[last_index].creation_date -history[i].creation_date).days} days {(history[last_index].creation_date -history[i].creation_date).seconds // 3600} hours {(history[last_index].creation_date -history[i].creation_date).seconds / 60} minutes")
        if (timezone.now()- history[i].creation_date).days >= days:
            break
        elif days/364 >= 1: #case for yearly data
            # print('years')
            if (history[last_index].creation_date -history[i].creation_date).days >=1:
                health_checks.append(history[i])
                last_index=i
                continue
        elif days / 28 >= 1:
            # print('weeks')
            if (history[last_index].creation_date - history[i].creation_date).seconds // 3600 >= 12:
                health_checks.append(history[i])
                last_index = i
                continue
        elif days / 14 >= 1:
            # print('weeks')
            if (history[last_index].creation_date - history[i].creation_date).seconds // 3600 >= 6:
                health_checks.append(history[i])
                last_index = i
                continue
        elif days / 7 >= 1:
            # print('weeks')
            if (history[last_index].creation_date - history[i].creation_date).seconds //3600 >= 2:
                health_checks.append(history[i])
                last_index = i
                continue
        elif days / 5 >= 1: #show every 15 minutes
            if (history[last_index].creation_date - history[i].creation_date).seconds / 60 >= 60:
                health_checks.append(history[i])
                last_index = i
                continue
        else: #show every 15 minutes
            if (history[last_index].creation_date - history[i].creation_date).seconds / 60 >= 5:
                health_checks.append(history[i])
                last_index = i
                continue


    health_checks.reverse()
    print(f"loaded {len(health_checks)} report histories")
    return build_line_chart_data(health_checks )


def build_line_chart_data(health_check_metrics):
    #presumably our data should be a list of lists in which list[n][0] is the label for the data and list[n][1] is the datapoint at the interval
    # fuck = {}
    data = []
    print(len(health_check_metrics))
    for metric in health_check_metrics:
        # print(json.loads(history.data)[1:])
        data.append([str(metric.creation_date).split('.')[0], 1 if metric.successful else -1])
        # fuck[str(metric.creation_date).split('.')[0]] ={str(metric.creation_date):1 if metric.successful else -1}
    labels =[]
    datasets =[]
    dumb = []
    for d  in data:
        labels.append(d[0])
        dumb.append(d[1])


    print(labels)
    print(datasets)
    return {"datasets":[{"label":f"{health_check_metrics[0].health_check.name} (1 pass, -1 fail)", "data":dumb, 'fill':True,'fillColor':'white', "tension":"0.1","borderColor": "blue"}], "labels":labels}