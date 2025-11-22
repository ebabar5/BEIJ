from app.schemas.product import Product
from typing import List
from app.repositories.products_repo import load_all
from app.services.filtering import filter_product_list, parse_filter_string


def keyword_search(keywords:List[str],strict:bool=False,filter:str|None=None) -> List[Product]:

    products = load_all()
    result = list()

    if not filter is None:
        filter_dict = parse_filter_string(filter)
        products = filter_product_list(products,**filter_dict)
                
    for product in products:
        #Uses spaces and commas to divide listing names, search should be case insensitive
        first_split = set(it.lower() for it in product["product_name"].split(" "))
        name_check = list()

        for word in first_split:
            if "," in word:
                name_check.extend(word.split(","))
            else:
                name_check.append(word)

        name_check = set(name_check)
        category_check = set(it.lower() for it in product["category"])
        
        if strict:
            word_match = 0
            cat_match = 0
            for word in keywords:
                if word.lower() in name_check:
                    word_match += 1
                if word.lower() in category_check:
                    cat_match += 1
            if word_match == len(keywords) or cat_match > len(product["category"])/2:
                result.append(product)

        else:
            for word in keywords:
                if word.lower() in name_check:
                    result.append(product)
                    break
                elif word.lower() in category_check:
                    result.append(product)
                    break
    
    return result