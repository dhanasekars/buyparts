"""
Created on : 15/04/22 4:52 PM
@author : ds
"""



import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


from selenium.webdriver.chrome.options import Options
URL = "https://buyparts.online/"
count = None
chrome_driver_path = "/Users/ds/Documents/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get(URL)
mega_menu_content_object = driver.find_elements(By.CSS_SELECTOR, "a" ".ss_megamenu_head")
print(mega_menu_content_object)
menu = 'https://buyparts.online/pages/replacement-parts-and-components-for-international-trucks'
driver.get(menu)
html = driver.find_element(By.TAG_NAME, 'html')
html.send_keys(Keys.END)
count_products = driver.find_elements_by_css_selector(".collection-grid-item__title")
total_parts = 0
for count_product in count_products:
    count = int(count_product.text.split('(')[1].split(" ")[1])
    total_parts = total_parts+count
print(total_parts)
driver.quit()

