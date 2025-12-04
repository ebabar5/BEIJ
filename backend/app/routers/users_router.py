from fastapi import APIRouter, status, Header, HTTPException, Query

from app.schemas.user import UserCreate, UserResponse, UserLogin, LoginResponse, UserUpdate
from app.services.user_service import (
    create_user, 
    authenticate_user,
    authenticate_admin,
    save_item, 
    unsave_item, 
    get_saved_item_ids,
    get_user_profile,
    update_user_profile
)
from app.services.token_service import invalidate_token
from app.services.view_history_service import add_view, get_view_history
from app.services.recommendation_service import get_recommendations
from app.schemas.product import Product
from typing import List

# Router for all user-related endpoints
# Includes authentication (register/login/logout), profile management, and saved items
router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate):
    """Register a new user"""
    return create_user(payload)

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login_user(payload: UserLogin):
    """Login user"""
    return authenticate_user(payload)

@router.post("/admin/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def admin_login(payload: UserLogin):
    return authenticate_admin(payload)

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout_user(authorization: str = Header(None)):
    """Logout user by invalidating their token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required.")
    
    # Extract the token from the Authorization header
    token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
    invalidate_token(token)
    return {"message": "Logged out successfully"}

# Specific routes must come before parameterized routes
# View history and recommendations endpoints (before /{user_id})
@router.post("/{user_id}/view-history/{product_id}", status_code=status.HTTP_200_OK)
def track_product_view(user_id: str, product_id: str):
    """Track a product view for a user"""
    view_history = add_view(user_id, product_id)
    return {"user_id": user_id, "recently_viewed": view_history}

@router.get("/{user_id}/view-history", status_code=status.HTTP_200_OK)
def get_view_history_user(user_id: str):
    """Get user's viewing history"""
    view_history = get_view_history(user_id)
    return {"user_id": user_id, "recently_viewed": view_history}

@router.get("/{user_id}/recommendations", response_model=List[Product], status_code=status.HTTP_200_OK)
def get_user_recommendations(
    user_id: str,
    exclude_product_id: str = Query(None, description="Product ID to exclude from recommendations"),
    limit: int = Query(8, ge=1, le=20, description="Maximum number of recommendations to return")
):
    """Get product recommendations for a user"""
    recommendations = get_recommendations(user_id, limit=limit, exclude_product_id=exclude_product_id)
    return recommendations

@router.post("/{user_id}/saved-items/{product_id}")
def save_item_user(user_id: str, product_id: str):
    """Save an item to user's saved list"""
    saved_ids = save_item(user_id, product_id)
    return {"user_id": user_id, "saved_item_ids": saved_ids}

@router.delete("/{user_id}/saved-items/{product_id}")
def unsave_item_user(user_id: str, product_id: str):
    """Remove an item from user's saved list"""
    saved_ids = unsave_item(user_id, product_id)
    return {"user_id": user_id, "saved_item_ids": saved_ids}

@router.get("/{user_id}/saved-items")
def get_saved_items_user(user_id: str):
    """Get user's saved items"""
    saved_ids = get_saved_item_ids(user_id)
    return {"user_id": user_id, "saved_item_ids": saved_ids}

# Parameterized routes must come after specific routes
@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_profile(user_id: str):
    return get_user_profile(user_id)

@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_profile(user_id: str, payload: UserUpdate):
    return update_user_profile(user_id, payload)

