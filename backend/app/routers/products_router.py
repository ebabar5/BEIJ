from fastapi import APIRouter, status, Query
from typing import List, Optional

from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.services.product_service import (
    list_products, 
    create_product, 
    delete_product, 
    update_product, 
    get_product_by_id
)

# Create a router instance with a prefix and tags
# The prefix means all routes here start with "/api/v1/products"
# Tags group these endpoints in the API docs
router = APIRouter(
    prefix="/api/v1/products",
    tags=["products"]
)

@router.get("/", response_model=List[Product])
def get_products(
    sort_by: Optional[str] = Query(
        default=None, 
        description="Optional sort order. Supported values: name, price_asc, price_desc, rating_desc"
    )
):
    """Get all products with optional sorting"""
    return list_products(sort_by=sort_by)

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def post_product(payload: ProductCreate):
    """Create a new product"""
    return create_product(payload)

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: str):
    """Get a single product by ID"""
    return get_product_by_id(product_id)

@router.put("/{product_id}", response_model=Product)
def put_product(product_id: str, payload: ProductUpdate):
    """Update an existing product"""
    return update_product(product_id, payload)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_product(product_id: str):
    """Delete a product"""
    delete_product(product_id)
    return None

