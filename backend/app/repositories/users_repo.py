from pathlib import Path
import json, os
from typing import List, Dict, Any, Optional 

from app.error_handling import NotFound

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