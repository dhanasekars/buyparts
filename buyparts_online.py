""" 
Created on : 14/04/22 9:03 PM
@author : ds  
"""

# Using selenium driver scrap buyparts.online and get details of the all parts available in the site.

# TODO : Page navigation and getting product details
# TODO : Get the total parts available in the website

import csv
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# TODO : Fix this using try catch, create a file with headers if file does not exist

# with open("buyparts.csv", "w") as file:
#     file_writer = csv.writer(file)
#     file_writer.writerow(COLUMN_HEADERS)

options = Options()
options.add_argument("--headless")
options.add_argument('--disable-gpu')


class BuyPartsOnline:
    def __init__(self):
        self.COLUMN_HEADERS = ('Category', 'Parts', 'Product Name', 'Product Type', 'Product Details',
                               'Offer Price','Old Price', 'Warranty')
        self.URL = "https://buyparts.online/"
        self.record = None
        self.selling_price = None
        self.old_price = None
        self.warranty = None
        self.product_name = None
        self.product_type = None
        self.product_detail = None
        self.vendor = None
        self.products_title_object = None
        self.chrome_driver_path = "/Users/ds/Documents/chromedriver"
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path, chrome_options=options)
        self.driver.get(self.URL)
        self.mega_menu_content_object = None
        self.mega_menu_content = None
        self.mega_menu_content_object = self.driver.find_elements_by_css_selector("a" ".ss_megamenu_head")
        self.parts_collection_grid = None
        self.parts_collection_grid_object = None
        self.mega_menu_title = None
        self.mega_menu_content = None
        self.part_menu_title = None
        self.products = None

    def get_mega_menu_urls(self):
        """
        Opens the URL and looks for objects of class '.ss_megamenu_head' and gets the anchor tag text
        :return: A List of mega menu url
        """
        # self.mega_menu_content = [uri.get_attribute('href') for uri in self.mega_menu_content_object]
        self.mega_menu_content = \
            ['https://buyparts.online/pages/replacement-parts-and-components-for-peterbilt-trucks']
        return self.mega_menu_content

    def get_parts_collection_grid_url(self, menu):
        self.driver.get(menu)
        self.mega_menu_title = self.driver. \
            find_element_by_css_selector('#breadcrumbs > div > div > nav > ol > li.active > span > span').text
        self.parts_collection_grid_object = self.driver.find_elements_by_css_selector("a" ".collection-grid-item__link")
        self.parts_collection_grid = [uri.get_attribute('href') for uri in self.parts_collection_grid_object]
        return self.parts_collection_grid

    def get_product_url(self, part):
        self.driver.get(part)
        self.part_menu_title = self.driver. \
            find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/section/div/div/nav/ol/li[2]/span/span').text
        self.products_title_object = self.driver.find_elements_by_css_selector("a" ".product-name")
        self.products = [uri.get_attribute('href') for uri in self.products_title_object]
        return self.products

    def get_product_details(self, product):
        self.driver.get(product)
        self.product_detail = self.driver.find_element_by_class_name("grcap_anchor_product").text
        self.vendor = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[4]/div[1]/div/div/div/div[1]/div/div[1]/div[2]/div[1]/div[3]/p[1]/a').text
        self.product_name = self.driver.find_element_by_class_name("product-single__title").text
        self.product_type = self.driver.find_element_by_class_name("product-single__type").text.split(":")[1].strip()
        self.warranty = self.driver.find_element_by_xpath(
            '//*[@id="ProductSection-product-template"]/div/div[1]/div[2]/div[1]/div[3]/p[4]').text.split(":")[1]\
            .strip()
        self.selling_price = self.driver.find_element_by_xpath('//*[@id="ProductPrice-product-template"]/span').text
        self.old_price = self.driver.find_element_by_xpath('//*[@id="ComparePrice-product-template"]/span').text
        # create a tuple of data for each product and append to result tuple
        self.record = (self.mega_menu_title, self.part_menu_title, self.product_name, self.product_type,
                       self.product_detail, self.selling_price, self.old_price, self.warranty)
        return self.record

    def close_driver(self):
        self.driver.quit()


buy_parts = BuyPartsOnline()
for mega_menu in buy_parts.get_mega_menu_urls():
    for parts_collection_grid in buy_parts.get_parts_collection_grid_url(mega_menu):
        for product_url in buy_parts.get_product_url(parts_collection_grid):
            result = []
            for product_details in buy_parts.get_product_details(product_url):
                result.append(product_details)
            print(result)
buy_parts.close_driver()


