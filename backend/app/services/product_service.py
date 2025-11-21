import uuid
from typing import List, Dict, Any, Optional 
from fastapi import HTTPException
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.repositories.products_repo import load_all, save_all
PLACEHOLDER = "N/A"

def with_placeholders(rec: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(rec)

    for key in ("product_name", "category", "discount_percentage", "about_product", "user_id",
                "user_name", "review_id", "review_content", "img_link", "product_link"):
        v = out.get(key)
        if v is None or (isinstance(v, str) and not v.strip()):
            out[key] = PLACEHOLDER

    rate_c = out.get("rating_count")
    if rate_c is None or (isinstance(rate_c, str) and not rate_c.strip()): 
        out["rating_count"] = 0
    else:
        try:
            out["rating_count"] = int(str(rate_c).replace(",", "").strip())
        except Exception:
            out["rating_count"] = 0
    return out


def list_products(sort_by: Optional[str] = None) -> List[Product]:
    items = [Product(**with_placeholders(it)) for it in load_all()]
    if sort_by is None or sort_by == "name":
        return sorted(items, key = lambda p: p.product_name.lower())

    if sort_by == "price_asc":
        return sorted(items, key = lambda p: p.discounted_price)

    if sort_by == "price_desc":
        return sorted(items, key = lambda p: p.discounted_price, reverse = True)

    if sort_by == "rating_desc": # put higher rating first
        return sorted(
            items,
            key = lambda p: (p.rating, p.rating_count), # if same, put rating_count first
            reverse = True,
        )
    raise HTTPException(
        status_code = 400,
        detail = (f"There is an issue with sort_by '{sort_by}'. "
        "Support values: name, price_asc, price_desc, rating_desc."
        ),
    )


def create_product(payload: ProductCreate) -> Product:
    products = load_all()
    new_id = str(uuid.uuid4())
    if any(it.get("id") == new_id for it in products):  # extremely unlikely, but consistent check
        raise HTTPException(status_code=409, detail="ID collision; retry.")
    new_product = Product(id=new_id,
                          product_name=payload.product_name.strip(),
                          category=payload.category,
                          discounted_price=payload.discounted_price,
                          actual_price=payload.actual_price,
                          discount_percentage=payload.discount_percentage.strip(),
                          rating=payload.rating,
                          rating_count=payload.rating_count,
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
    for it in load_all():
        if it.get("product_id") == product_id:
            return Product(**with_placeholders(it))
    raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found")

def update_product(product_id: str, payload: ProductUpdate) -> Product:
    products = load_all()
    for idx, it in enumerate(products):
        if it.get("product_id") == product_id:
            updated = Product(
                id=product_id,
                product_name=payload.product_name.strip(),
                category=payload.category,
                discounted_price=payload.discounted_price,
                actual_price=payload.actual_price,
                discount_percentage=payload.discount_percentage.strip(),
                rating=payload.rating,
                rating_count=payload.rating_count,
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
    new_products = [it for it in products if it.get("product_id") != product_id]
    if len(new_products) == len(products):
        raise HTTPException(status_code=404, detail=f"Protect '{product_id}' not found")
    save_all(new_products)

