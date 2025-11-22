import uuid
from typing import List, Dict, Any, Optional 
from fastapi import HTTPException
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.repositories.products_repo import load_all, save_all
from app.constants.http_status import BAD_REQUEST, NOT_FOUND, CONFLICT
PLACEHOLDER = "N/A"

PLACEHOLDER_FIELDS = (
    "product_name",
    "category",
    "discount_percentage",
    "about_product",
    "user_id",
    "user_name",
    "review_id",
    "review_content",
    "img_link",
    "product_link",
)

AVAILABLE_SORTS = ("name", "price_asc", "price_desc", "rating_desc")

def _normalize_rating_count(raw: Any) -> int:
    if raw is None or (isinstance(raw, str) and not raw.strip()):
        return 0
    try:
        return int(str(raw).replace(",", "").strip())
    except Exception:
        return 0


def with_placeholders(rec: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(rec)
    for key in PLACEHOLDER_FIELDS:
        v = out.get(key)
        if v is None or (isinstance(v, str) and not v.strip()):
            out[key] = PLACEHOLDER
    out["rating_count"] = _normalize_rating_count(out.get("rating_count"))
    return out

def _load_products_models() -> List[Product]:
    return [Product(**with_placeholders(it)) for it in load_all()]

def _key_name(p: Product):
    return p.product_name.lower()

def _key_price(p: Product):
    return p.discounted_price

def _key_rating(p: Product):
    return (p.rating, p.rating_count)

def list_products(sort_by: Optional[str] = None) -> List[Product]:
    items = _load_products_models()

    sort_key = "name" if sort_by is None else sort_by

    match sort_key:
        case "name":
            return sorted(items, key=_key_name)

        case "price_asc":
            return sorted(items, key=_key_price)

        case "price_desc":
            return sorted(items, key=_key_price, reverse=True)

        case "rating_desc":
            return sorted(items, key=_key_rating, reverse=True)

        case _:
            raise HTTPException(
                status_code=BAD_REQUEST,
                detail=(
                    f"There is an issue with sort_by '{sort_by}'. "
                    "Support values: name, price_asc, price_desc, rating_desc."
                ),
            )

def _build_product(product_id: str, payload: ProductCreate | ProductUpdate) -> Product:
    return Product(
        product_id=product_id,
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
        review_title=payload.review_title,
        review_content=payload.review_content.strip(),
        img_link=payload.img_link.strip(),
        product_link=payload.product_link.strip(),
    )

def create_product(payload: ProductCreate) -> Product:
    products = load_all()
    new_id = str(uuid.uuid4())

    if any(it.get("product_id") == new_id for it in products):
        raise HTTPException(status_code=CONFLICT, detail="ID collision; retry.")

    new_product = _build_product(new_id, payload)
    products.append(new_product.dict())
    save_all(products)
    return new_product


def get_product_by_id(product_id: str) -> Product:
    for it in load_all():
        if it.get("product_id") == product_id:
            return Product(**with_placeholders(it))
    raise HTTPException(status_code=NOT_FOUND, detail=f"Product '{product_id}' not found")

def update_product(product_id: str, payload: ProductUpdate) -> Product:
    products = load_all()
    for idx, it in enumerate(products):
        if it.get("product_id") == product_id:
            updated = _build_product(product_id, payload)
            products[idx] = updated.dict()
            save_all(products)
            return updated
    raise HTTPException(status_code=NOT_FOUND, detail=f"Product '{product_id}' not found")

def delete_product(product_id: str) -> None:
    products = load_all()
    new_products = [it for it in products if it.get("product_id") != product_id]
    if len(new_products) == len(products):
        raise HTTPException(status_code=NOT_FOUND, detail=f"Protect '{product_id}' not found")
    save_all(new_products)

