from pathlib import Path
import json, os
from typing import List, Dict, Any, Optional 

from app.error_handling import NotFound # use error_handling

DATA_PATH= Path(__file__).resolve().parents[1] / "data" / "users.json"
def load_all() -> List[Dict[str,Any]]:
    if not DATA_PATH.exists():
        return []
    with DATA_PATH.open("r", encoding="utf-8") as f:
       return json.load(f)
def save_all(items: List[Dict[str, Any]]) -> None:
    tmp = DATA_PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    os.replace(tmp, DATA_PATH)

# return a single user dict by id with saved_item_ids 
def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    users = load_all()
    for user in users:
        if user.get("user_id") == user_id:
            # put saved_item_ids to a list
            saved = user.get("saved_item_ids")
            if not isinstance(saved, list):
                user["saved_item_ids"] = []
            return user
    return None

# add product_id to the users saved item ids, ensuring it is not already added
def add_saved_item(user_id: str, product_id: str) -> Dict[str, Any]:
    users = load_all()
    for user in users:
        if user.get("user_id") == user_id:
            saved = user.get("saved_item_ids")
            if not isinstance(saved, list):
                saved = []
            if product_id not in saved:
                saved.append(product_id)  # add product id
            user["saved_item_ids"] = saved
            save_all(users)
            return user
    raise NotFound("User not found") # from error_handling


# remove product id from saved item ids
def remove_saved_item(user_id: str, product_id: str) -> Dict[str, Any]:
    users = load_all()
    for user in users:
        if user.get("user_id") == user_id:
            saved = user.get("saved_item_ids")
            if not isinstance(saved, list):
                saved = []
            if product_id in saved:
                saved.remove(product_id)  
            user["saved_item_ids"] = saved
            save_all(users)
            return user
    raise NotFound("User not found") # from error_handling

# return copy of users saved item ids list 
def get_saved_item_ids(user_id: str) -> List[str]:
    user = get_user_by_id(user_id)
    if user is None:
        # from error_handling 
        raise NotFound("User not found")
    saved = user.get("saved_item_ids")
    if not isinstance(saved, list):
        saved = []
    # return a simple copy so callers can't change the internal state
    return list(saved)