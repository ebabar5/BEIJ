from typing import List
from app.schemas.product_preview import ProductPreview
from app.repositories.products_repo import load_all
from fastapi import HTTPException

def get_all_product_previews() -> List[ProductPreview]:
    products = load_all()
    previews = []
    for it in products:
        arg_list = {"product_id":it["product_id"],
                    "product_name":it["product_name"],
                    "discounted_price":it["discounted_price"],
                    "rating":it["rating"]}
        previews.append(ProductPreview(**arg_list))
    return previews

