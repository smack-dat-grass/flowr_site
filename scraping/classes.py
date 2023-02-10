import traceback

from selenium.common import TimeoutException


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
    # def open_connection(self):
    #     raise NotImplementedError
    # def close_connection(self):
    #     raise NotImplementedError
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
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