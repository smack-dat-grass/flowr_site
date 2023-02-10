import json
from django.utils.timezone import now
from locations.models import City, State
from dispensaries.models import Dispensary
# from scraping.functions  import build_webdriver, load_dispensaries
from config.models import Connection,WEBSOURCE_CONNECTOR_TYPE
import importlib
# from scraping.classes import D
#so basically queue up the locations we want to run for
for connection in Connection.objects.filter(type=WEBSOURCE_CONNECTOR_TYPE):

    module = importlib.import_module("scraping.classes")
    class_ = getattr(module, json.loads(connection.attributes)['class'])
    # instance =
    scraper = class_(connection)
    scraper.build_webdriver()
    for city in City.objects.filter(state=State.objects.filter(code='MI')[0]).order_by('last_refreshed')[:5]:
        # driver = build_webdriver()
        if not city.state.legal:
            continue
        print(f"Loading dispensaries for {str(city)}")
        dispos = scraper.load_dispensaries(str(city))
        print(f"Found {len(dispos.keys())} in {str(city)}")

        for dispo, data in dispos.items():

            if len([x for x in Dispensary.objects.filter(name=dispo, url=data['url'])]) ==0: #basically prevent us from having duplicate dispensaries

                dispensary = Dispensary()
                dispensary.name=dispo
                dispensary.save()
                dispensary.city.add(city)
                dispensary.image=data['image']
                dispensary.url=data['url']
            else:
                dispensary= Dispensary.objects.get(name=dispo, url=data['url'])
                dispensary.image = data['image']
                dispensary.url = data['url']
            dispensary.save()
        city.last_refreshed=now()

        city.save()
