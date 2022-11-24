import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re
from shopee_crawler import parser

class ShopeeCrawler:
    product_keys = [
        'url', 
        'name', 
        'min_price', 
        'max_price', 
        'pre_price', 
        'location', 
        'historical_sold', 
        'vouchers', 
        'ratings', 
        'image'
    ]
    
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless") # Ensure GUI is off
        options.add_argument("--no-sandbox")
        options.binary_location = "/usr/bin/google-chrome"
        chrome_driver_binary = "/home/ngthuan/Windows/chromedriver"
        self.driver = webdriver.Chrome(chrome_driver_binary, options=options)

    def crawl_by_url(self, search_url):
        print(f'Connecting to {search_url}...')
        self.driver.get(search_url)
        WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_4FDN71')))

        # Scroll few times to load all items
        print('Getting page information...')
        for x in range(30):
            self.driver.execute_script("window.scrollBy(0,300)")
            time.sleep(0.1)
        
        all_items = self.driver.find_elements(By.XPATH, '//a[@data-sqe="link"]')
        products = []
        for item in all_items:
            product = {}
            for key in self.product_keys:
                setattr(sys.modules[__name__], key, getattr(parser, f'parse_{key}_from_element')(item))
                product[key] = getattr(sys.modules[__name__], key)

            print(product)                
            print('-'*15)
            
        print('Found total:',len(all_items), 'items')
        return products
    