from typing import List
from app.schemas.product_preview import ProductPreview
from app.schemas.product import Product
from app.repositories.products_repo import load_all
from fastapi import HTTPException

def parse_to_previews(target:List[Product]) -> List[ProductPreview]:
    previews = []
    for it in target:
        arg_list = {"product_id":it["product_id"],
                    "product_name":it["product_name"],
                    "discounted_price":it["discounted_price"],
                    "rating":it["rating"]}
        previews.append(ProductPreview(**arg_list))
    return previews

def get_all_product_previews() -> List[ProductPreview]:
    return parse_to_previews(load_all())

from app.services.filtering import filter_product_list

def filter_previews(filter_string:str) -> List[ProductPreview]:
    #TODO implement a 406 not acceptable error for malformed filter strings
    category_string = ""
    parts = filter_string.split("&")
    category_string = parts[0]
    filtered_products = []
    try:
        if len(parts)>1:
            max = 0
            min = 0
            rating = 0.0
            if parts[1][:4] == "max=":
                max = int(parts[1][4:])
            if len(parts)>2:
                if parts[2][:4] == "min=":
                    min = int(parts[2][4:])
            filtered_products = filter_product_list(load_all(),category_string,min,max)

        else:
            filtered_products = filter_product_list(load_all(),category_string)
        return parse_to_previews(filtered_products)
    except Exception:
        raise HTTPException(status_code=406,detail="Malformed Filter Request")

    
