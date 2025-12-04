from datetime import datetime
from typing import List, Dict, Any
from app.repositories.users_repo import load_all, save_all, get_user_by_id
from app.error_handling import NotFound
from fastapi import HTTPException

MAX_VIEW_HISTORY = 20

def add_view(user_id: str, product_id: str) -> List[Dict[str, str]]:
    """Add a product view to user's viewing history"""
    users = load_all()
    user = None
    
    for u in users:
        if u.get("user_id") == user_id:
            user = u
            break
    
    if user is None:
        raise NotFound(f"User '{user_id}' not found.")
    
    # Initialize recently_viewed if it doesn't exist
    if "recently_viewed" not in user:
        user["recently_viewed"] = []
    
    recently_viewed = user.get("recently_viewed", [])
    
    # Remove existing entry for this product (if any) to avoid duplicates
    recently_viewed = [v for v in recently_viewed if v.get("product_id") != product_id]
    
    # Add new view with current timestamp
    recently_viewed.insert(0, {
        "product_id": product_id,
        "viewed_at": datetime.utcnow().isoformat()
    })
    
    # Keep only the most recent MAX_VIEW_HISTORY items
    if len(recently_viewed) > MAX_VIEW_HISTORY:
        recently_viewed = recently_viewed[:MAX_VIEW_HISTORY]
    
    user["recently_viewed"] = recently_viewed
    save_all(users)
    
    return recently_viewed

def get_view_history(user_id: str) -> List[Dict[str, str]]:
    """Get user's viewing history"""
    user = get_user_by_id(user_id)
    if user is None:
        raise NotFound(f"User '{user_id}' not found.")
    
    return user.get("recently_viewed", [])

