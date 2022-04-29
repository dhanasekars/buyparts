""" 
Created on : 29/04/22 5:42 PM
@author : ds  
"""

from buyparts_online import BuyPartsOnline


buy_parts = BuyPartsOnline(url="https://buyparts.online")
# buy_parts.get_all_product_details()

mega_total = 0
for mega_menu in buy_parts.get_mega_menu_urls():
    total = buy_parts.get_total_parts(mega_menu)
    mega_total = mega_total + total
print(mega_total)


buy_parts.close_driver()

