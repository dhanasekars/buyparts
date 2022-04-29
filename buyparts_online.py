""" 
Created on : 14/04/22 9:03 PM
@author : ds  
"""

# Using selenium driver scrap buyparts.online and get details of the all parts available in the site.

# TODO : Total parts count as class method [ Now it's partial done ]
# TODO : Page navigation and getting product details
# TODO : Add unit tests for each method

import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

COLUMN_HEADERS = ('Category', 'Parts', 'Product Name', 'Product Type', 'Product Details',
                  'Offer Price', 'Old Price', 'Warranty')

# Creates a file and add the header column when the file is not present.
try:
    with open("buyparts.csv", "r") as file:
        pass
except FileNotFoundError:
    with open("buyparts.csv", "w") as file:
        file_writer = csv.writer(file)
        file_writer.writerow(COLUMN_HEADERS)

options = Options()
options.add_argument("--headless")
options.add_argument('--disable-gpu')


class BuyPartsOnline:
    def __init__(self, url):
        self.URL = url
        self.chrome_driver_path = "/Users/ds/Documents/chromedriver"
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path, chrome_options=options)
        self.driver.get(url)
        self.mega_menu = None
        self.count_products = None
        self.record = None
        self.selling_price = None
        self.old_price = None
        self.warranty = None
        self.product_name = None
        self.product_type = None
        self.product_detail = None
        self.vendor = None
        self.products_title_object = None
        self.mega_menu_content_object = None
        self.mega_menu_content = None
        self.mega_menu_content_object = self.driver.find_elements(By.CSS_SELECTOR, "a" ".ss_megamenu_head")
        self.parts_collection_grid = None
        self.parts_collection_grid_object = None
        self.mega_menu_title = None
        self.mega_menu_content = None
        self.part_menu_title = None
        self.products = None
        self.count = 0

    def get_mega_menu_urls(self):
        """
        Opens the URL and looks for objects of class '.ss_megamenu_head' and gets the anchor tag text
        :return: A List of mega menu url
        """
        # self.mega_menu_content = [uri.get_attribute('href') for uri in self.mega_menu_content_object]
        self.mega_menu_content = \
            ['https://buyparts.online/pages/replacement-parts-and-components-for-western-star-trucks']
        return self.mega_menu_content

    def get_parts_collection_grid_url(self, menu):
        """
        param menu: url - from mega menu, returned by fn - > get_mega_menu_urls
        :return: parts collection grid url
        """
        self.driver.get(menu)
        self.mega_menu_title = self.driver. \
            find_element(By.CSS_SELECTOR, '#breadcrumbs > div > div > nav > ol > li.active > span > span').text
        self.parts_collection_grid_object = \
            self.driver.find_elements(By.CSS_SELECTOR, "a" ".collection-grid-item__link")
        self.parts_collection_grid = [uri.get_attribute('href') for uri in self.parts_collection_grid_object]
        return self.parts_collection_grid

    def get_product_url(self, part):
        """

        :param part: url - from parts grid, returned by fn -> get_parts_collection_grid_url
        :return: url of a product page
        """
        self.driver.get(part)
        self.part_menu_title = self.driver. \
            find_element(By.XPATH, '/html/body/div[1]/div[4]/div[1]/section/div/div/nav/ol/li[2]/span/span').text
        self.products_title_object = self.driver.find_elements(By.CSS_SELECTOR, "a" ".product-name")
        self.products = [uri.get_attribute('href') for uri in self.products_title_object]
        return self.products

    def get_product_details(self, product):
        """

        :param product: url - from product page, returned by fn -> get_product_url
        :return: a tuple -> product details
        """
        self.driver.get(product)
        self.product_detail = self.driver.find_element(By.CLASS_NAME, "grcap_anchor_product").text
        self.vendor = self.driver.find_element(By.XPATH,
                                               '/html/body/div[1]/div[4]/div[1]/div/div/div/div[1]/div/div[1]/div[2]'
                                               '/div[1]/div[3]/p[1]/a').text
        self.product_name = self.driver.find_element(By.CLASS_NAME, "product-single__title").text
        self.product_type = self.driver.find_element(By.CLASS_NAME, "product-single__type").text.split(":")[1].strip()
        self.warranty = self.driver.find_element(By.XPATH,
                                                 '//*[@id="ProductSection-product-template"]/div/div[1]/div[2]/div[1]'
                                                 '/div[3]/p[4]').text.split(":")[1].strip()
        self.selling_price = self.driver.find_element(By.XPATH, '//*[@id="ProductPrice-product-template"]/span').text
        self.old_price = self.driver.find_element(By.XPATH, '//*[@id="ComparePrice-product-template"]/span').text
        # create a tuple of data for each product and append to result tuple
        self.record = (self.mega_menu_title, self.part_menu_title, self.product_name, self.product_type,
                       self.product_detail, self.selling_price, self.old_price, self.warranty)
        return self.record

    def get_total_parts(self, menu) -> int:
        self.driver.get(menu)
        html = self.driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)
        count_products = self.driver.find_elements(By.CSS_SELECTOR, ".collection-grid-item__title")
        total_parts = 0
        for count_product in count_products:
            count = int(count_product.text.split('(')[1].split(" ")[1])
            total_parts = total_parts + count
        return total_parts

    def get_all_product_details(self):
        for mega_menu in BuyPartsOnline.get_mega_menu_urls(self):
            for parts_collection_grid in BuyPartsOnline.get_parts_collection_grid_url(self, menu=mega_menu):
                result = []
                for product_url in BuyPartsOnline.get_product_url(self, parts_collection_grid):
                    result.append(BuyPartsOnline.get_product_details(self, product_url))
                with open("buyparts.csv", "a") as f:
                    fwriter = csv.writer(f)
                    for row in result:
                        fwriter.writerow(row)

    def close_driver(self):
        """

        :return: Nothing. Closes the selenium driver
        """
        self.driver.quit()
