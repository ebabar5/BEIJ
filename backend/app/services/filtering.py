from app.schemas.product import Product
from typing import List, Dict

def filter_product_list(target:List[Product],cat_string:str,min_price:int=0,max_price:int=0):
    max_price = max(max_price,0)
    min_price = max(min_price,0)

    if min_price > max_price:
        temp = max_price
        max_price = min_price
        min_price = temp
    
    cat_filtered = []

    if cat_string == "all" or cat_string == "":
        cat_filtered = target
    else:
        categories = cat_string.split("*")
        for product in target:
            added = False
            for category in categories:
                if(category in product["category"]) and not added:
                    cat_filtered.append(product)
                    added = True
    
    result = []

    if min_price == 0 and max_price == 0:
        result = cat_filtered
    else:
        for product in cat_filtered:
            price = product["discounted_price"]
            if price <= max_price and price >= min_price:
                result.append(product)

    return result


def parse_filter_string(filter_string:str) -> Dict:
    #Parse a filter string into category string, min-price, max-price
    return_dict = dict()
    parts = filter_string.split("&")
    return_dict["cat_string"] = parts[0] #The category string is the first item in the return list
    if len(parts)>1:
        #rating = 0.0 could add min rating filter later
        for part in parts[1:]:
            if part[:4] == "max=":
                return_dict["max_price"] = int(part[4:])
                continue
            if parts[2][:4] == "min=":
                return_dict["min_price"] = int(part[4:])
                continue
    
    return return_dict