from fastapi import APIRouter, status
from typing import List
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.services.product_service import list_products, create_product, delete_product, update_product

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=List[Product])
def get_products():
    return list_products()

#simple post the payload (is the body of the request)
@router.post("", response_model=Product, status_code=201)
def post_product(payload: ProductCreate):
    return create_product(payload)

from app.services.products_service import list_products, create_product, get_product_by_id

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: str):
    return get_product_by_id(product_id)

## We use put here because we are not creating an entirely new product, ie. we keep id the same
@router.put("/{product_id}", response_model=Product)
def put_product(product_id: str, payload: ProductUpdate):
    return update_product(product_id, payload)


## we put the status there becuase in a delete, we wont have a return so it indicates it happened succesfully
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_product(product_id: str):
    delete_product(product_id)
    return None