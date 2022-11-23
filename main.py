# from shopee_crawler import crawler

# crawler_tool = crawler.Crawler()
# crawler_tool.set_origin('shopee.vn')
# data = crawler_tool.crawl_by_search(keyword='iphone 13')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re

options = webdriver.ChromeOptions()
options.add_argument("--headless") # Ensure GUI is off
options.add_argument("--no-sandbox")
options.binary_location = "/usr/bin/google-chrome"
chrome_driver_binary = "/home/ngthuan/Windows/chromedriver"
driver = webdriver.Chrome(chrome_driver_binary, options=options)

url = 'https://shopee.vn/search?keyword=iphone%2013'
print(f'Connecting to {url}...')
driver.get(url)
WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_4FDN71')))

# Scroll few times to load all items
print('Getting page information...')
for x in range(30):
    driver.execute_script("window.scrollBy(0,300)")
    time.sleep(0.1)

# SCROLL_PAUSE_TIME = 2
# # Get scroll height
# last_height = driver.execute_script("return document.body.scrollHeight")
# while True:
#     # Scroll down to bottom
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#     # Wait to load page
#     time.sleep(SCROLL_PAUSE_TIME)

#     # Calculate new scroll height and compare with last scroll height
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height
 
all_items = driver.find_elements(By.XPATH, '//a[@data-sqe="link"]')
all_urls = []
for item in all_items:
    url = item.get_attribute('href')
    name = item.find_element(By.XPATH, './/div[@class="ie3A+n bM+7UW Cve6sh"]').text
    price = item.find_elements(By.XPATH, './/span[@class="ZEgDH9"]')
    min_price = price[0].text
    if len(price) > 1:
        max_price = price[1].text
    else:
        max_price = None
    
    sell_place = item.find_element(By.XPATH, './/div[@class="zGGwiV"]').text
    try:
        voucher_element = item.find_element(By.XPATH, './/div[@class="FD2XVZ"]')
        vouchers = voucher_element.find_elements(By.XPATH, './/div')
        vouchers = [voucher.text for voucher in vouchers]
    except:
        vouchers = []
        
    try:    
        pre_price = item.find_element(By.XPATH, './/div[@class="vioxXd ZZuLsr d5DWld"]').text
    except:
        pre_price = ""
    
    try:
        historical_sold = item.find_element(By.XPATH, './/div[@class="r6HknA uEPGHT"]').text
    except:
        historical_sold = 'Đã bán 0'
    rating_stars = item.find_elements(By.XPATH, './/div[@class="shopee-rating-stars__lit"]')
    ratings = 0
    for rating_star in rating_stars:
        star_width = re.match(r'width: (.*)%;', rating_star.get_attribute('style')).group(1)
        ratings += float(star_width)/100
    ratings = round(ratings, 1)
    print(name)
    print(vouchers)
    print('\u0336'.join(pre_price) + '\u0336')
    print(min_price,'-',max_price)
    print(historical_sold)
    print(sell_place)
    print(ratings)
    
    
    print('-'*15)
#     # print(image_info.text)
    
#     # break
#     # print(url)
    
print('Found total:',len(all_items), 'items')