from app.schemas.product import Product
from typing import List

def filter_product_list(target:List[Product],cat_string:str,min_price:int=0,max_price:int=0):

    #Convert any negative values to zero
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
        #TODO parse category string and apply filter
        pass
    
    result = []

    if min_price == 0 and max_price == 0:
        result = cat_filtered
    else:
        #TODO apply price filtering
        pass

    return result