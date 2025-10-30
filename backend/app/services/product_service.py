import uuid
from typing import List, Dict, Any
from fastapi import HTTPException
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.repositories.products_repo import load_all, save_all


def list_products() -> List[Product]:
    return [Product(**it) for it in load_all()]

def create_product(payload: ProductCreate) -> Product:
    products = load_all()
    new_id = str(uuid.uuid4())
    if any(it.get("id") == new_id for it in products):  # extremely unlikely, but consistent check
        raise HTTPException(status_code=409, detail="ID collision; retry.")
    new_product = Product(id=new_id,
                          product_name=payload.product_name.strip(),
                          category=payload.category,
                          discounted_price=payload.discounted_price.strip(),
                          actual_price=payload.actual_price.strip(),
                          discount_percentage=payload.discount_percentage.strip(),
                          rating=payload.rating.strip(),
                          rating_count=payload.rating_count.strip(),
                          about_product=payload.about_product.strip(),
                          user_id=payload.user_id,
                          user_name=payload.user_name,
                          review_id=payload.review_id,
                          review_content=payload.review_content.strip(),
                          img_link=payload.img_link.strip(),
                          product_link=payload.product_link.strip())
    products.append(new_product.dict())
    save_all(products)
    return new_product

def get_product_by_id(product_id: str) -> Product:
    products = load_all()
    for it in products:
        if it.get("id") == product_id:
            return Product(**it)
    raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found")

def update_product(product_id: str, payload: ProductUpdate) -> Product:
    products = load_all()
    for idx, it in enumerate(products):
        if it.get("id") == product_id:
            updated = Product(
                id=product_id,
                product_name=payload.product_name.strip(),
                category=payload.category,
                discounted_price=payload.discounted_price.strip(),
                actual_price=payload.actual_price.strip(),
                discount_percentage=payload.discount_percentage.strip(),
                rating=payload.rating.strip(),
                rating_count=payload.rating_count.strip(),
                about_product=payload.about_product.strip(),
                user_id=payload.user_id,
                user_name=payload.user_name,
                review_id=payload.review_id,
                review_content=payload.review_content.strip(),
                img_link=payload.img_link.strip(),
                product_link=payload.product_link.strip()
            )
            products[idx] = updated.dict()
            save_all(products)
            return updated
    raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found")

def delete_product(product_id: str) -> None:
    products = load_all()
    new_products = [it for it in products if it.get("id") != product_id]
    if len(new_products) == len(products):
        raise HTTPException(status_code=404, detail=f"Protect '{product_id}' not found")
    save_all(new_products)

