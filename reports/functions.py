import random,json
from config.classes import OracleConnector, MySQLConnector, LDAPConnector, APIConnector,PostgreGreenplumConnector
from config.models import  Connection, API_CONNECTOR_TYPE, ORACLE_CONNECTOR_TYPE,LDAP_CONNECTOR_TYPE,MYSQL_CONNECTOR_TYPE,POSTGRE_CONNECTOR_TYPE
import numpy, traceback
# from tasks.functions import create_alert
from django.utils import timezone

from .models import ReportHistory
# timezone.now()
def random_color():
    return "%06x" % random.randint(0, 0xFFFFFF)

# def build_chartjs_bar_data(report_history):
#     results = json.loads(report_history.data)
#     del results[0]
#     data = {'labels':[], 'datasets':[{}]}
#     data['datasets'][0]['label']=report_history.report.name
#     data['datasets'][0]['backgroundColor']="rgba(204, 0, 0, .4)"
#     data['datasets'][0]['borderColor']="#c00"
#     data['datasets'][0]['borderWidth']=2
#     data['datasets'][0]['hoverBackgroundColor']="#59597F"
#     data['datasets'][0]['data']=[]
#     print(results)
#     for row in results:
#         data['labels'].append(row[0])
#         data['datasets'][0]['data'].append(row[1])
#
#     return data

# def build_chartjs_pie_data(report_history):
#     results = json.loads(report_history.data)
#
#
#     del results[0]
#     data = {'labels': [[x[0] for x in results]], 'datasets': [{}]}
#     data['datasets'][0]['label'] = report_history.report.name
#     data['datasets'][0]['backgroundColor'] = [f'#{random_color()}' for x in results]
#     data['datasets'][0]['data'] = [int(x[1]) for x in results]
#     return data
#     pass
def build_chartjs_line_data(report_histories):
    #presumably our data should be a list of lists in which list[n][0] is the label for the data and list[n][1] is the datapoint at the interval
    fuck = {}
    # print(len(report_histories))
    for history in report_histories:
        # print(json.loads(history.data)[1:])
        fuck[str(history.creation_date).split('.')[0]] ={x[0]: x[1] for x in json.loads(history.data)[1:]}
    labels =[]
    datasets =[]
    for key, value in fuck.items():
        labels.append(key)
        for k, v in value.items():
            if next((item for item in datasets if item["label"] == k), None) is not None:
                datasets[next((i for i, item in enumerate(datasets) if item["label"] == k), None)]['data'].append(v)

            else:
                point_color = random_color()
                color = list(numpy.random.choice(range(256), size=3))
                d = {
                    "backgroundColor": f"rgb({color[0]},{color[1]},{color[2]})",
                    "borderColor": f"rgb({color[0]},{color[1]},{color[2]})",
                    "fill": False,
                    # "backgroundColor": point_color,
                    # "borderColor":point_color,
                        "label":k,
                        # "fill":False,
                        "data": [v]
                    }
                datasets.append(d)
    # print(labels)
    # print(datasets)
    return {"datasets":datasets, "labels":labels}

    # datasets = []
    # labels= []
    # for i in range(0, report_histories):
    #     entry = report_histories[i]
    #     point_color = random_color()
    #     report_data = json.loads(entry.attributes)
    #     datapoints = []
    #
    #     d = {
    #             "label": report_histories[i][0],
    #             "fillColor": "blue",
    #             "strokeColor": "red",
    #             "pointColor": point_color,
    #             "pointStrokeColor": point_color,
    #             "pointHighlightFill": "white",
    #             "pointHighlightStroke": "black",
    #             "data": datapoints
    #         }
    #     datasets.append(d)
    # return {"datasets":datasets, "labels":labels}

def run_report(report):
    if report.connection.type==ORACLE_CONNECTOR_TYPE: #handle oracle case
        ora_conn = OracleConnector(Connection.objects.get(name=report.connection.name))
        ora_conn.open_connection()
        error= False
        try:
            ora_conn.run_report(report)
            ora_conn.close_connection()
        except:
            error=True
            ora_conn.close_connection()
        if error:
            raise  Exception(traceback.format_exc())
    if report.connection.type==MYSQL_CONNECTOR_TYPE:
        mysql_conn = MySQLConnector(Connection.objects.get(name=report.connection.name))
        mysql_conn.open_connection()
        error = False
        try:
            mysql_conn.run_report(report)
            mysql_conn.close_connection()
        except:
            error=True
            mysql_conn.close_connection()
        if error:
            raise Exception(traceback.format_exc())


    if report.connection.type == LDAP_CONNECTOR_TYPE:
        ldap_conn = LDAPConnector(Connection.objects.get(name=report.connection.name))
        ldap_conn.open_connection()
        error=False
        try:
            ldap_conn.run_report(report)
            ldap_conn.close_connection()
        except:
            error=True
            ldap_conn.close_connection()
        if error:
            raise Exception(traceback.format_exc())
    if report.connection.type==API_CONNECTOR_TYPE:
        try:
            result = []
            connection = APIConnector(Connection.objects.get(name=report.connection.name))
            print(report.code)
            exec(report.code)

        except Exception as e:
            # import traceback
            traceback.print_exc()
            print('we ran into an error')
            print(traceback.format_exc())
            raise Exception(str(e))
    if report.connection.type==POSTGRE_CONNECTOR_TYPE:
        postgre_conn = PostgreGreenplumConnector(Connection.objects.get(name=report.connection.name))
        postgre_conn.open_connection()
        error = False
        try:
            postgre_conn.run_report(report)
            postgre_conn.close_connection()
        except:
            error=True
            postgre_conn.close_connection()
        if error:
            raise Exception(traceback.format_exc())

def build_tabulator_basic_data(input_data):
    data = []
    report_attrs = input_data
    # print(report_attrs[0])
    for i in range(1, len(report_attrs)):
        entry = {}
        for ii in range(0, len(report_attrs[i])):
            entry[report_attrs[0][ii]]=report_attrs[i][ii]
        data.append(entry)
    return data

def build_chartjs_pie_data(input_data):
    data = {"labels":[], "datasets":[{"data":[],"label":"", "data":[],"backgroundColor":[], "hoverOffset":4}]}
    # labels: [
    #     'Red',
    #     'Blue',
    #     'Yellow'
    # ],
    # datasets: [{
    #     label: 'My First Dataset',
    #     data: [300, 50, 100],
    #     backgroundColor: [
    #         'rgb(255, 99, 132)',
    #         'rgb(54, 162, 235)',
    #         'rgb(255, 205, 86)'
    #     ],
    #     hoverOffset: 4
    # }]
    # report_attrs = input_data
    for i in range(1, len(input_data)):
        # data['labels'].append(input_data[i][0])
        data['datasets'][0]['data'].append(input_data[i][1])
        data['labels'].append(input_data[i][0])
        # point_color = random_color()
        color = list(numpy.random.choice(range(256), size=3))
        data['datasets'][0]['backgroundColor'].append(f"rgb({color[0]},{color[1]},{color[2]})")

    # for i in range(1, len(report_attrs)):
    #     entry = {}
    #     for ii in range(0, len(report_attrs[i])):
    #         entry[report_attrs[0][ii]]=report_attrs[i][ii]
    #     data.append(entry)
    # print(data)
    return data

def build_chartjs_bar_data(input_data):
    data = {"labels":[input_data[i][0] for i in range(1, len(input_data))], "datasets":[]}
    # labels: [
    #     'Red',
    #     'Blue',
    #     'Yellow'
    # ],
    # datasets: [{
    #     label: 'My First Dataset',
    #     data: [300, 50, 100],
    #     backgroundColor: [
    #         'rgb(255, 99, 132)',
    #         'rgb(54, 162, 235)',
    #         'rgb(255, 205, 86)'
    #     ],
    #     hoverOffset: 4
    # }]
    # report_attrs = input_data
    # for i in range(1, len(input_data)):
    entry ={}
    color = list(numpy.random.choice(range(256), size=3))
    entry['label']=input_data[0][1]
    entry['backgroundColor']=f"rgb({color[0]},{color[1]},{color[2]})"
    entry['data']=[input_data[i][1] for i in range(1, len(input_data))]
    data['datasets'].append(entry)
    # data['labels'].append(input_data[i][0])
        # data['datasets'][0]['data'].append(input_data[i][1])
        # data['datasets'][0]['data'].append(input_data[i][1])
        # data['labels'].append(input_data[i][0])
        # point_color = random_color()

        # data['datasets'][0]['backgroundColor'].append()

    # for i in range(1, len(report_attrs)):
    #     entry = {}
    #     for ii in range(0, len(report_attrs[i])):
    #         entry[report_attrs[0][ii]]=report_attrs[i][ii]
    #     data.append(entry)
    # print(data)
    return data



def build_line_chart_data(label, input_data):
    #presumably our data should be a list of lists in which list[n][0] is the label for the data and list[n][1] is the datapoint at the interval
    # fuck = {}
    data = []
    # print(len(input_data))
    # for metric in input_data:
        # print(json.loads(history.data)[1:])
        # data.append([str(metric.creation_date).split('.')[0], 1 if metric.successful else -1])
        # fuck[str(metric.creation_date).split('.')[0]] ={str(metric.creation_date):1 if metric.successful else -1}
    labels =[]
    datasets =[]
    dumb = []
    for d  in input_data:
        labels.append(d[0])
        dumb.append(d[1])


    print(labels)
    print(datasets)
    return {"datasets":[{"label":f"{label}", "data":dumb, 'fill':True,'fillColor':'white', "tension":"0.1","borderColor": "blue"}], "labels":labels}