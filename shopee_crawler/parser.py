from selenium.webdriver.common.by import By
import re

FIELD_CLASS_MAP = {
    'name':             'ie3A+n bM+7UW Cve6sh',
    'price':            'ZEgDH9',
    'location':         'zGGwiV', 
    'vouchers':         'FD2XVZ', 
    'pre_price':        'vioxXd ZZuLsr d5DWld',
    'historical_sold':  'r6HknA uEPGHT',
    'ratings':          'shopee-rating-stars__lit',
    'image':            'yvbeD6 KUUypF'
}
def parse_url_from_element(item):
    return item.get_attribute('href')

def parse_name_from_element(item):
        return item.find_element(By.XPATH, F'.//div[@class="{FIELD_CLASS_MAP["name"]}"]').text
    
def parse_min_price_from_element(item):
    price = item.find_elements(By.XPATH, f'.//span[@class="{FIELD_CLASS_MAP["price"]}"]')
    min_price = int(price[0].text.replace('.',''))
    return min_price

def parse_max_price_from_element(item):
    price = item.find_elements(By.XPATH, f'.//span[@class="{FIELD_CLASS_MAP["price"]}"]')
    if len(price) > 1:
        max_price = int(price[1].text.replace('.',''))
    else:
        max_price = None
    return max_price

def parse_location_from_element(item):
    return item.find_element(By.XPATH, f'.//div[@class="{FIELD_CLASS_MAP["location"]}"]').text

def parse_vouchers_from_element(item):
    try:
        voucher_element = item.find_element(By.XPATH, f'.//div[@class="{FIELD_CLASS_MAP["vouchers"]}"]')
        vouchers = voucher_element.find_elements(By.XPATH, './/div')
        vouchers = [voucher.text for voucher in vouchers]
    except:
        vouchers = []
    return vouchers

def parse_pre_price_from_element(item):
    try:    
        pre_price = float(item.find_element(By.XPATH, f'.//div[@class="{FIELD_CLASS_MAP["pre_price"]}"]').text)
    except:
        pre_price = None
        
    return pre_price

def parse_historical_sold_from_element(item):
    try:
        historical_sold = item.find_element(By.XPATH, f'.//div[@class="{FIELD_CLASS_MAP["historical_sold"]}"]').text
        historical_sold = historical_sold.split(' ')[-1]
    except:
        historical_sold = 0
        
    return historical_sold

def parse_ratings_from_element(item):
    rating_stars = item.find_elements(By.XPATH, f'.//div[@class="{FIELD_CLASS_MAP["ratings"]}"]')
    ratings = 0
    for rating_star in rating_stars:
        star_width = re.match(r'width: (.*)%;', rating_star.get_attribute('style')).group(1)
        ratings += float(star_width)/100
    ratings = round(ratings, 1)
    return ratings

def parse_image_from_element(item):
    image = item.find_element(By.XPATH, f'.//div[@class="{FIELD_CLASS_MAP["image"]}"]/img')
    return image.get_attribute('src')