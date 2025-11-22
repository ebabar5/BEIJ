from app.schemas.product import Product
from typing import List, Optional
from app.repositories.products_repo import load_all
from app.services.filtering import filter_product_list, parse_filter_string


def _tokenize_name(name: str) -> set[str]:
    # split on spaces and then split any comma-joined tokens
    tokens: List[str] = []
    for w in name.lower().split():
        tokens.extend(w.split(","))
    return set(t for t in tokens if t)


def keyword_search(
    keywords: List[str],
    strict: bool = False,
    filter: Optional[str] = None
    ) -> List[Product]:
    
    products = load_all()
    if filter is not None:
        filter_dict = parse_filter_string(filter)
        products = filter_product_list(products, **filter_dict)

    kw = [k.lower() for k in keywords]
    result: List[Product] = []

    for product in products:
        name_tokens = _tokenize_name(product["product_name"])
        category_tokens = set(c.lower() for c in product["category"])

        if strict:
            word_match = sum(k in name_tokens for k in kw)
            cat_match = sum(k in category_tokens for k in kw)

            if word_match == len(kw) or cat_match > len(product["category"]) / 2:
                result.append(product)

        else:
            if any(k in name_tokens or k in category_tokens for k in kw):
                result.append(product)

    return result
