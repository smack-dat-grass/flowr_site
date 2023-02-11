import json
import traceback
from products.classes import ProductType
from selenium.common import TimeoutException

from selenium.webdriver.support import expected_conditions as ec

class WebSource:
    driver = None
    connection =None
    def __init__(self, connection):
        self.connection = connection
    def test_connection(self):
        raise NotImplementedError
    def build_webdriver(self):
        raise NotImplementedError
    def load_dispensaries(self, location):
        raise NotImplementedError

    def load_products(self):
        raise NotImplementedError
    def scrap_data(self):
        raise NotImplementedError

    def process_thc_deals(self,  products, dispensary, product_type=ProductType.FLOWER):
        raise NotImplementedError
    # def open_connection(self):
    #     raise NotImplementedError
    # def close_connection(self):
    #     raise NotImplementedError
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# from functions import  load_module_config,strip_special_chars,strip_alphabetic_chars,read_csv, write_csv as _write_csv
from tabulate import tabulate
# from ready_up import  initialize
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
class Dutchie(WebSource):

    def build_webdriver(self):
        CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        CHROMEDRIVER_PATH = '../chromedriver'
        WINDOW_SIZE = "1920,1080"
        print()
        chrome_options = Options()
        chrome_options.headless = True
        chrome_options.add_argument("--start-minimized")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

        self.driver = webdriver.Chrome(executable_path='../chromedriver', chrome_options=chrome_options)
        self.driver.set_window_size(1920, 1080)
        # driver = webdriver.Chrome('../chromedriver')
        self.driver.get(self.connection.host)
        age_restriction_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[data-test="age-restriction-yes"]')
        age_restriction_btn.click()


    def load_dispensaries(self, location):
        wait = WebDriverWait(self.driver, 30)
        self.driver.get(self.connection.host)
        search_bar = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[data-testid="homeAddressInput"]')))[0]
        # search_bar = self.driver.find_element(By.CSS_SELECTOR, 'input[data-testid="homeAddressInput"]')
        search_bar.send_keys(location)

        # locations = driver.find_elements(By.CSS_SELECTOR, 'div[class="option__Container-sc-1e884xj-0 khOZsM"]')
        search_bar.click()
        # class="dispensary-card__Image-sc-1wd9p5b-2 fKTDvr"
        # time.sleep(10)
        location = wait.until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[data-testid="addressAutocompleteOption"]')))[0]
        wait.until(ec.element_to_be_clickable(location))
        time.sleep(3)
        location.click()

        # soup = BeautifulSoup(driver.page_source)
        # results = soup.find_all("li", {"data-testid":"addressAutocompleteOption"})
        # results = soup.find("a", data-testid='listbox--1')
        try:
            images = wait.until(ec.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'img[class="dispensary-card__Image-sc-1wd9p5b-2 fKTDvr"]')))
        except TimeoutException:
            # print(traceback)
            traceback.print_exc()
            if "There are no dispensaries available for pickup nearby" in self.driver.page_source:

                return {}

        # for image in images:
        #     print(image.get_attribute('src'))
        dispensary_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="dispensary-card"]')
        dispensaries = {}
        for i in range(0, len(dispensary_links)):  # in dispensary_links:
            link = dispensary_links[i]
            dispensaries[
                link.text.split("\n")[0] if link.text.split("\n")[0] != 'Closed' else link.text.split("\n")[1]] = {
                "url": link.get_attribute('href'), "distance": link.text.split("\n")[-2].split(" Mile")[0],
                "image": images[i].get_attribute('src')}
            # dis = [x.get_attribute('href') for x in dispensaries]
        # print(f"Found {len(dispensaries.keys())} dispenaries in {location}")
        # self.driver.get(self.connection.host)
        return dispensaries

    def load_products(self):
        wait = WebDriverWait(self.driver,30)

        for i in range(0,20):
            # for element  in driver.find_element(By.CSS_SELECTOR, 'html[data-js-focus-visible=""]'):
            self.driver.find_element(By.CSS_SELECTOR, 'html[data-js-focus-visible=""]').send_keys(Keys.PAGE_DOWN)
            # html.send_keys(Keys.PAGE_DOWN)
            # time.sleep(3)
        wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'img[class="product-image__LazyLoad-sc-16rwjkk-0 busNCP desktop-product-list-item__Image-sc-8wto4u-2 ipJspp lazyloaded"]')))
        # ?page = 2
        products = self.scrape_data(self.driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="product-list-item"]'))
        # gt_100 = len(products) > 99
        # page = page+1
        pages = WebDriverWait(self.driver, 30).until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="media-query__ContentDiv-sc-18mweoi-0 hrGTDA"]')))
        del pages[0]
        del pages[-1]
        product_url = self.driver.current_url
        # while gt_100:
        try:
            for i in range(2,max([int(x.text) for x in pages])+1):
                page = i
                print(f"Loading page {page} of {self.driver.current_url}")
                # f"{dispens/ary.url}{json.loads(self.connection.attributes)['urls'][kwargs['type']]}"
                stripped_url =product_url.split("?")[0]
                self.driver.get(f"{stripped_url}?page={page}")
                for i in range(0, 20):
                    # for element  in driver.find_element(By.CSS_SELECTOR, 'html[data-js-focus-visible=""]'):
                    self.driver.find_element(By.CSS_SELECTOR, 'html[data-js-focus-visible=""]').send_keys(
                        Keys.PAGE_DOWN)
                    # html.send_keys(Keys.PAGE_DOWN)
                    # time.sleep(3)
                _products = wait.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR,'img[class="product-image__LazyLoad-sc-16rwjkk-0 busNCP desktop-product-list-item__Image-sc-8wto4u-2 ipJspp lazyloaded"]')))
                # _products = self.load_products(page)
                products = self.scrape_data(_products) + products
        except:
            traceback.print_exc()

            # deals += self.scrape_data(_products)


        return products

    def scrape_data(self,data):
        results = []
        for element in data:
            try:
                results.append(element.text.replace("\n",json.loads(self.connection.attributes)['delimiter']))
            except:
                traceback.print_exc()
                print(f"could not load data for element {element.text}")
        return results

    def process_thc_deals(self, products, dispensary, product_type=ProductType.FLOWER):
        thc_objects = []
        for deal in products:
            if 'thc' not in deal.lower():
                continue
            # print(deal)
            product= {}
            data = deal.split(json.loads(self.connection.attributes)['delimiter'])
            # product = Product()

            product['raw'] = data
            while data[0] in ['Staff Pick', 'Special offer'] or '$' in data[0]:
                del data[0]
            product['dispensary'] = dispensary
            product['producer'] = data[0]
            product['name'] = data[1]

            try:
                if data[2].lower() not in ['indica', 'sativa', 'hybrid', 'high cbd']:
                    data.insert(2, 'n/a')
                    # print('hmm')
                product ['type'] = data[2]
            except:
                traceback.print_exc()

                continue  # skip if this is the case
            try:
                if "|" in data[3]:
                    product['thc'] = data[3].split('|')[0].strip().split("THC: ")[-1]
                else:
                    product['thc'] = data[3].strip().split("THC: ")[-1]
            except:
                traceback.print_exc()
                pass
            # if '%'data[-1]:

            if '%' in data[-1]:
                product['price'] = data[-2]
                if type == ProductType.EDIBLES:
                    product['quantity'] = '1'
                else:
                    product['quantity'] = data[-3] if '$' not in data[-3] else data[-4]

            else:
                product['price'] = data[-1]
                if type == ProductType.EDIBLES:
                    product['quantity'] = '1'
                else:
                    product['quantity'] = data[-2]
            # print(deal)
            # print(product)
            # if type==ProductType.EDIBLES:
            #     try:
            #         product.smooth_edible_data()
            #     except:
            #         traceback.print_exc()
            #         pass
            thc_objects.append(product)
        # product.save()
        # thc_object.calculate_10mg_cost()
        return thc_objects