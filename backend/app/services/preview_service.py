from typing import List
from app.schemas.product_preview import ProductPreview
from app.schemas.product import Product
from app.repositories.products_repo import load_all
from fastapi import HTTPException
from app.services.filtering import parse_filter_string

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
    filtered_products = []
    try:
        filter_dict = parse_filter_string(filter_string)
        filtered_products = filter_product_list(load_all(),**filter_dict)

        return parse_to_previews(filtered_products)
    except Exception:
        raise HTTPException(status_code=406,detail="Malformed Filter Request")

    
