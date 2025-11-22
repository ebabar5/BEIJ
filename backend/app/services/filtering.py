from typing import List, Dict, Any

def _normalize_prices(min_price: int, max_price: int) -> tuple[int, int]:
    # keep exact behavior: clamp to 0 then swap if reversed
    min_price = max(min_price, 0)
    max_price = max(max_price, 0)
    if min_price > max_price:
        min_price, max_price = max_price, min_price
    return min_price, max_price

def filter_product_list(
    target: List[Dict[str, Any]],
    cat_string: str,
    min_price: int = 0,
    max_price: int = 0
):
    min_price, max_price = _normalize_prices(min_price, max_price)
    # Category filtering
    if cat_string == "all" or cat_string == "":
        cat_filtered = target
    else:
        categories = set(cat_string.split("*"))
        cat_filtered = [
            product for product in target
            if any(category in product["category"] for category in categories)
        ]

    # Price filtering
    if min_price == 0 and max_price == 0:
        return cat_filtered

    return [
        product for product in cat_filtered
        if min_price <= product["discounted_price"] <= max_price
    ]

def parse_filter_string(filter_string: str) -> Dict:
    # Parse a filter string into category string, min-price, max-price
    return_dict = dict()
    parts = filter_string.split("&")
    return_dict["cat_string"] = parts[0]  # The category string is the first item in the return list
    if len(parts) > 1:
        # rating = 0.0 could add min rating filter later
        for part in parts[1:]:
            if part[:4] == "max=":
                return_dict["max_price"] = int(part[4:])
                continue
            if parts[2][:4] == "min=":
                return_dict["min_price"] = int(part[4:])
                continue
                
    return return_dict
