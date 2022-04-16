""" 
Created on : 15/04/22 4:52 PM
@author : ds  
"""


from selenium import webdriver

chrome_driver_path = "/Users/ds/Documents/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
# URL = "https://buyparts.online/"

products = 'https://buyparts.online/products/674-6028'
driver.get(products)
product_detail = driver.find_element_by_class_name("grcap_anchor_product")
vendor = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div/div/div/div[1]/div/div[1]/div[2]/div[1]/div[3]/p[1]/a')
product_name = driver.find_element_by_class_name("product-single__title")
product_type = driver.find_element_by_class_name("product-single__type")
warranty = driver.find_element_by_xpath('//*[@id="ProductSection-product-template"]/div/div[1]/div[2]/div[1]/div[3]/p[4]')
selling_price = driver.find_element_by_xpath('//*[@id="ProductPrice-product-template"]/span')
old_price = driver.find_element_by_xpath('//*[@id="ComparePrice-product-template"]/span')
print(vendor.text)
print(product_name.text)
print(product_type.text)
print(warranty.text)
print(selling_price.text)
print(old_price.text)
print(product_detail.text)




driver.quit()