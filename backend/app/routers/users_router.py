from fastapi import APIRouter, status, Header, HTTPException, Query
from typing import List

from app.schemas.user import (
    UserCreate, 
    UserResponse, 
    UserLogin, 
    LoginResponse, 
    UserUpdate,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ResetPasswordRequest,
    ResetPasswordResponse
)
from app.schemas.product import Product
from app.services.user_service import (
    create_user, 
    create_admin_user,
    authenticate_user,
    authenticate_admin,
    save_item, 
    unsave_item, 
    get_saved_item_ids,
    get_user_profile,
    update_user_profile,
    list_users,
    generate_reset_token,
    reset_password_with_token,
    add_recently_viewed,
    get_recently_viewed_products
)
from app.services.token_service import invalidate_token
# Router for all user-related endpoints
# Includes authentication (register/login/logout), profile management, and saved items
router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)

@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users():
    """Get all users (admin only)"""
    return list_users()

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

@router.post("/admin/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_admin(payload: UserCreate, admin_secret: str = Query(..., description="Admin secret required to create admin users")):
    """Register a new admin user (requires admin secret)"""
    return create_admin_user(payload, admin_secret)

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout_user(authorization: str = Header(None)):
    """Logout user by invalidating their token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required.")
    
    # Extract the token from the Authorization header
    token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
    invalidate_token(token)
    return {"message": "Logged out successfully"}


@router.post("/forgot-password", response_model=ForgotPasswordResponse, status_code=status.HTTP_200_OK)
def forgot_password(payload: ForgotPasswordRequest):
    """Generate a password reset token for the given email.
    In production, this token would be sent via email.
    For demo purposes, it's returned in the response."""
    return generate_reset_token(payload.email)


@router.post("/reset-password", response_model=ResetPasswordResponse, status_code=status.HTTP_200_OK)
def reset_password(payload: ResetPasswordRequest):
    """Reset password using a valid reset token"""
    return reset_password_with_token(payload.token, payload.new_password)

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_profile(user_id: str):
    return get_user_profile(user_id)

@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_profile(user_id: str, payload: UserUpdate):
    return update_user_profile(user_id, payload)

@router.get("/{user_id}", response_model=UserResponse)
def get_user_profile_endpoint(user_id: str):
    """
    GET /api/v1/users/{user_id}
    Used by profile-management + error-handling tests.
    """
    return get_user_profile(user_id)
    
@router.put("/{user_id}", response_model=UserResponse)
def update_user_profile_endpoint(user_id: str, payload: UserUpdate):
    """
    PUT /api/v1/users/{user_id}
    Updates username / email / password.
    """
    return update_user_profile(user_id, payload)


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

@router.post(
    "/{user_id}/recently-viewed/{product_id}",
    summary="Add recently viewed item",
)
def add_recently_viewed_endpoint(user_id: str, product_id: str):
    rv_ids = add_recently_viewed(user_id, product_id)
    return {"user_id": user_id, "recently_viewed_ids": rv_ids}


@router.get(
    "/{user_id}/recently-viewed",
    response_model=List[Product],
    summary="Get recently viewed products",
)
def get_recently_viewed_endpoint(
    user_id: str,
    limit: int = Query(
        4,
        ge=1,
        le=20,
        description="Max number of recently viewed items to return",
    ),
):
    return get_recently_viewed_products(user_id, limit=limit)

