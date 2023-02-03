import requests
from datetime import timedelta, datetime

import requests,json, traceback
attributes = json.loads(health_check.attributes)
today = datetime.now()
yesterday = today - timedelta(days=2)
url = f"https://api.covid19api.com/live/country/india/status/confirmed/date/{yesterday.strftime('%Y-%m-%d')}T00:00:00Z"
health_check_metric=HealthCheckMetric()
health_check_metric.health_check=health_check
# url="http://admin.idm.ge.com/"
try:
    r = requests.get(url, verify=False)
    print(r.status_code)
    if r.status_code != 200:
        print(f"Response from {url}: {r.status_code} {r.reason}")
        health_check_metric.message = "Could not load Covid-19 metrics for India"
        health_check_metric.icon = 'https://www.iconsdb.com/icons/preview/red/warning-xxl.png'
        health_check_metric.successful = False

    else:
        data = json.loads(r.text)
        pass
        total_case_count = 0
        cases_by_day = {}
        for entry in data:
            if entry['Date'] not in cases_by_day:
                cases_by_day[entry['Date']] = entry['Confirmed']
            else:
                cases_by_day[entry['Date']] = entry['Confirmed'] + cases_by_day[entry['Date']]
        dates = [x for x in reversed(sorted(cases_by_day.keys()))][-2:]
        delta = cases_by_day[dates[0]] - cases_by_day[dates[1]]
        if delta > attributes['threshold']:
            health_check_metric.message = f"{delta} new Covid-19 Cases Reported in India in the last 24 hours"
            health_check_metric.icon = 'https://www.iconsdb.com/icons/preview/red/warning-xxl.png'
            health_check_metric.successful = False
        else:
            health_check_metric.message = f"{delta} new Covid-19 Cases Reported in India in the last 24 hours"
            health_check_metric.icon = 'https://www.iconsdb.com/icons/preview/green/ok-xxl.png'
            health_check_metric.successful = True
        # health_check_metric.message = "CorpIDM is Up"
        # health_check_metric.icon = 'https://www.iconsdb.com/icons/preview/green/ok-xxl.png'
        # health_check_metric.successful = True

except Exception as e:

    proxy_dict = {}
    proxy_dict['http'] = "http://PITC-Zscaler-Americas-Cincinnati3PR.proxy.corporate.ge.com:80"
    proxy_dict['https']="http://PITC-Zscaler-Americas-Cincinnati3PR.proxy.corporate.ge.com:80"
    try:
        r = requests.get(url, proxies=proxy_dict, verify=False)
        if r.status_code != 200:
            health_check_metric.message = "Could not load Covid-19 metrics for India"
            health_check_metric.icon = 'https://www.iconsdb.com/icons/preview/red/warning-xxl.png'
            health_check_metric.successful = False
        else:
            data = json.loads(r.text)
            pass
            total_case_count = 0
            cases_by_day = {}
            for entry in data:
                if entry['Date'] not in cases_by_day:
                    cases_by_day[entry['Date']] = entry['Confirmed']
                else:
                    cases_by_day[entry['Date']] = entry['Confirmed'] + cases_by_day[entry['Date']]
            dates = [x for x in reversed(sorted(cases_by_day.keys()))][-2:]
            delta = cases_by_day[dates[0]] - cases_by_day[dates[1]]
            if delta > attributes['threshold']:
                health_check_metric.message = f"{delta} new Covid-19 Cases Reported in India in the last 24 hours"
                health_check_metric.icon = 'https://www.iconsdb.com/icons/preview/red/warning-xxl.png'
                health_check_metric.successful = False
            else:
                health_check_metric.message = f"{delta} new Covid-19 Cases Reported in India in the last 24 hours"
                health_check_metric.icon = 'https://www.iconsdb.com/icons/preview/green/ok-xxl.png'
                health_check_metric.successful = True
    except:

        health_check_metric.message = "Could not load Covid-19 metrics for India"
        health_check_metric.icon = 'https://www.iconsdb.com/icons/preview/red/warning-xxl.png'
        health_check_metric.successful = False


health_check_metric.save()
