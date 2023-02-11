import json
import time
import traceback

from config.functions import process_list_concurrently
from django.utils.timezone import now
from locations.models import City, State
from dispensaries.models import Dispensary
# from scraping.functions  import build_webdriver, load_dispensaries
from config.models import Connection,WEBSOURCE_CONNECTOR_TYPE
import importlib
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dope_deals_site.settings")
django.setup()
from products.classes import ProductType
from products.models import Product
# from scraping.classes import D
def load_dispensary_data(cities, kwargs):



    #so basically queue up the locations we want to run for
    for connection in Connection.objects.filter(type=WEBSOURCE_CONNECTOR_TYPE):
        # def process_list_concurrently(data, process_function, batch_size):
        module = importlib.import_module("scraping.classes")
        class_ = getattr(module, kwargs['class'])
        # instance =
        scraper = class_(connection)
        scraper.build_webdriver()
        # for city in cities:
        for i in range(0, len(cities)):
            city=cities[i]
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
                    dispensary.connection=connection
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
def load_product_data(dispensaries, kwargs):
    module = importlib.import_module("scraping.classes")
    class_ = getattr(module, kwargs['class'])
    scraper = class_(dispensaries[0].connection)
    scraper.build_webdriver()
    for i in range(0,len(dispensaries)):
        dispensary = dispensaries[i]
        # print(f"Loading {type} deals for {dispensary}")
        _url = f"{dispensary.url}{json.loads(dispensaries[0].connection.attributes)['urls'][kwargs['type']]}"
        scraper.driver.get(_url)
        print(f"Loading product data for {dispensaries[i]}")


        products = scraper.load_products()


        # driver.quit()
        for deal in scraper.process_thc_deals(products, dispensary,json.loads(dispensaries[0].connection.attributes)['urls'][kwargs['type']]):

            if len([x for x in Product.objects.filter(name=deal['name'],dispensary=dispensary)]) ==0:
                product = Product()
            else:
                product = Product.objects.filter(name=deal['name'],dispensary=dispensary)[0]
            product.dispensary=dispensary
            if kwargs['type'] == ProductType.FLOWER:
                product.type = ProductType.FLOWER
                # print('\n'.join([str(x) for x in strains]))
                # scrape_flower_products(products)
            elif kwargs['type'] == ProductType.PREROLLS:
                product.type = ProductType.PREROLLS
            # if:
            #     thc_object=THCObject()
            elif kwargs['type'] == ProductType.VAPORIZERS or kwargs['type'] == ProductType.CONCENTRATES:
                product.type = ProductType.PREROLLS
            elif kwargs['type'] == ProductType.EDIBLES:
                product.type = ProductType.EDIBLES
            else:
                raise Exception(f"Invalid product type: {kwargs['type']}")
            product.name=deal['name']
            product.price=deal['price']
            product.thc=deal['thc']
            product.quantity=deal['quantity']
            product.raw=deal['raw']
            product.producer=deal['producer']
            product.save()
        dispensary.last_refreshed=now()
        dispensary.save()

