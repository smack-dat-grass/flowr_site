import json
import time
from config.functions import process_list_concurrently
from django.utils.timezone import now
from locations.models import City, State
from dispensaries.models import Dispensary
# from scraping.functions  import build_webdriver, load_dispensaries
from config.models import Connection,WEBSOURCE_CONNECTOR_TYPE
import importlib
from scraping.functions import load_dispensary_data,load_product_data
# from scraping.classes import D
# start_time = time.time()
# #so basically queue up the locations we want to run for
for _type in json.loads(task.attributes)['product_types']:
    dispensaries = [x for x in  Dispensary.objects.all().order_by('last_refreshed')]
    # print(f"Processing {len(dispensaries)}")
    process_list_concurrently(dispensaries,load_product_data,json.loads(task.attributes)['load_size'], {"type":_type,'class':json.loads(dispensaries[0].connection.attributes)['class']})
