""" 
Created on : 14/04/22 9:03 PM
@author : ds  
"""

# Using selenium driver scrap buyparts.online and get details of the all parts available in the site.

# TODO : Page navigation and getting product details
# TODO : Get the total parts available in the website

import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
COLUMN_HEADERS = ('Category', 'Parts', 'Product Name', 'Product Type', 'Product Details', 'Offer Price',
                  'Old Price', 'Warranty')

# TODO : Fix this using try catch, create a file with headers if file does not exist

# with open("buyparts.csv", "w") as file:
#     file_writer = csv.writer(file)
#     file_writer.writerow(COLUMN_HEADERS)

options = Options()
options.add_argument("--headless")
options.add_argument('--disable-gpu')

chrome_driver_path = "/Users/ds/Documents/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=options)
URL = "https://buyparts.online/"

driver.get(URL)
# gets the main mega menu list
mega_menu_content_object = driver.find_elements_by_css_selector("a" ".ss_megamenu_head")
# mega_menu_content = [uri.get_attribute('href') for uri in mega_menu_content_object]
mega_menu_content = ['https://buyparts.online/pages/replacement-parts-and-components-for-mack-trucks']

for mega_menu in mega_menu_content:  # this loops there the main mega menu
    driver.get(mega_menu)
    mega_menu_title = driver.\
        find_element_by_css_selector('#breadcrumbs > div > div > nav > ol > li.active > span > span').text
    parts_collection_grid_object = driver.find_elements_by_css_selector("a" ".collection-grid-item__link")
    parts_collection_grid = [uri.get_attribute('href') for uri in parts_collection_grid_object]
    for part in parts_collection_grid:  # after getting into megamenu, loops through parts collection grid
        driver.get(part)
        part_menu_title = driver.\
            find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/section/div/div/nav/ol/li[2]/span/span').text
        products_title_object = driver.find_elements_by_css_selector("a" ".product-name")
        products = [uri.get_attribute('href') for uri in products_title_object]
        result = []
        for product in products:  # loop inside parts grid for each product
            driver.get(product)
            product_detail = driver.find_element_by_class_name("grcap_anchor_product").text
            vendor = driver.find_element_by_xpath(
                '/html/body/div[1]/div[4]/div[1]/div/div/div/div[1]/div/div[1]/div[2]/div[1]/div[3]/p[1]/a').text
            product_name = driver.find_element_by_class_name("product-single__title").text
            product_type = driver.find_element_by_class_name("product-single__type").text.split(":")[1].strip()
            warranty = driver.find_element_by_xpath(
                '//*[@id="ProductSection-product-template"]/div/div[1]/div[2]/div[1]/div[3]/p[4]').text.split(":")[1]\
                .strip()
            selling_price = driver.find_element_by_xpath('//*[@id="ProductPrice-product-template"]/span').text
            old_price = driver.find_element_by_xpath('//*[@id="ComparePrice-product-template"]/span').text
            # create a tuple of data for each product and append to result tuple
            record = (mega_menu_title, part_menu_title, product_name, product_type, product_detail,
                      selling_price, old_price, warranty)
            result.append(record)
        # write the tuple to the file after fetching all products for a single grid
        with open("buyparts.csv", "a") as file:
            file_writer = csv.writer(file)
            for row in result:
                file_writer.writerow(row)

driver.quit()
