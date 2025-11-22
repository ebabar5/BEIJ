from app.schemas.product import Product
from typing import List, Dict, Any

def filter_product_list(target: List[Product], cat_string: str, min_price: int = 0, max_price: int = 0):
    max_price = max(max_price, 0)
    min_price = max(min_price, 0)

    has_min = (min_price != 0)
    has_max = (max_price != 0)

    # only swap if BOTH bounds are actually provided
    if has_min and has_max and min_price > max_price:
        min_price, max_price = max_price, min_price

    # category filtering
    if cat_string == "all" or cat_string == "":
        cat_filtered = list(target)
    else:
        categories = cat_string.split("*")
        cat_filtered = []
        for product in target:
            for category in categories:
                if category in product["category"]:
                    cat_filtered.append(product)
                    break

    # price filtering
    if not has_min and not has_max:
        return cat_filtered

    result = []
    for product in cat_filtered:
        price = product["discounted_price"]

        if has_min and price < min_price:
            continue
        if has_max and price > max_price:
            continue

        result.append(product)

    return result


def parse_filter_string(filter_string: str) -> Dict[str, Any]:
    return_dict: Dict[str, Any] = {
        "cat_string": "",
        "min_price": 0,
        "max_price": 0,
    }

    if not filter_string:
        return return_dict

    parts = filter_string.split("&")
    return_dict["cat_string"] = parts[0]

    for part in parts[1:]:
        if part.startswith("max="):
            try:
                return_dict["max_price"] = int(part[4:])
            except ValueError:
                pass
        elif part.startswith("min="):
            try:
                return_dict["min_price"] = int(part[4:])
            except ValueError:
                pass

    return return_dict
