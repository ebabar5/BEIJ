from app.schemas.product import Product
from typing import List

def filter_product_list(target:List[Product],cat_string:str,min_price:int=0,max_price:int=0):

    #Convert any negative values to zero
    max_price = max(max_price,0)
    min_price = max(min_price,0)
    #If only a min or max is given the other value should be ignored
    no_min = False
    no_max = False
    if min_price == 0 and max_price != 0:
        no_min = True
    elif max_price == 0 and min_price != 0:
        no_max = True
    elif min_price > max_price:
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
            if no_max and price >= min_price:
                result.append(product)
            elif no_min and price <= max_price:
                result.append(product)
            elif price <= max_price and price >= min_price:
                result.append(product)

    return result