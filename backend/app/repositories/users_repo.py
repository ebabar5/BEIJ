from pathlib import Path
from typing import List, Dict, Any, Optional 
from app.error_handling import NotFound
from app.repositories.repository_helpers import load_json_data, save_json_data

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "users.json"

def load_all() -> List[Dict[str,Any]]:
    return load_json_data(DATA_PATH)

def save_all(items: List[Dict[str, Any]]) -> None:
    save_json_data(DATA_PATH, items)

def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    users = load_all()
    for user in users:
        if user.get("user_id") == user_id:
            saved = user.get("saved_item_ids")
            if not isinstance(saved, list):
                user["saved_item_ids"] = []
            return user
    return None

def add_saved_item(user_id: str, product_id: str) -> Dict[str, Any]:
    users = load_all()
    for user in users:
        if user.get("user_id") == user_id:
            saved = user.get("saved_item_ids")
            if not isinstance(saved, list):
                saved = []
            if product_id not in saved:
                saved.append(product_id)
            user["saved_item_ids"] = saved
            save_all(users)
            return user
    raise NotFound("User not found")

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
    raise NotFound("User not found")

def get_saved_item_ids(user_id: str) -> List[str]:
    user = get_user_by_id(user_id)
    if user is None:
        raise NotFound("User not found")
    saved = user.get("saved_item_ids")
    if not isinstance(saved, list):
        saved = []
    return list(saved)

def add_recently_viewed_item(user_id: str, product_id: str, max_items: int = 10) -> Dict[str, Any]:
    users = load_all()
    for user in users:
        if user.get("user_id") == user_id:
            rv = user.get("recently_viewed_ids")
            if not isinstance(rv, list):
                rv = []

            if product_id in rv:
                rv.remove(product_id)
            rv.insert(0, product_id)

            user["recently_viewed_ids"] = rv[:max_items]
            save_all(users)
            return user
    raise NotFound("User not found")


def get_recently_viewed_ids(user_id: str, limit: int = 4) -> List[str]:
    user = get_user_by_id(user_id)
    if user is None:
        raise NotFound("User not found")

    rv = user.get("recently_viewed_ids")
    if not isinstance(rv, list):
        rv = []
    return rv[:limit]
