from app.schemas.product import Product
from typing import List
from app.repositories.products_repo import load_all
from app.services.filtering import filter_product_list


def keyword_search(keywords:List[str],strict:bool=False,filter:str|None=None) -> List[Product]:

    products = load_all()
    result = list()

    if not filter is None:
        category_string = ""
        parts = filter.split("&")
        category_string = parts[0]
        max = 0
        min = 0
        if len(parts)>1:
            for part in parts[1:]:
                if part[:4] == "max=":
                    max = int(part[4:])
                    continue
                if parts[2][:4] == "min=":
                    min = int(part[4:])
                    continue
                
        products = filter_product_list(products,category_string,min,max)
                

    for product in products:
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