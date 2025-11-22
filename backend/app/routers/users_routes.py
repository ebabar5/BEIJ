from fastapi import APIRouter, status, Header, HTTPException
from app.schemas.user import UserCreate, UserResponse, UserLogin, LoginResponse, UserUpdate
from app.services.user_service import create_user, authenticate_user, authenticate_admin, save_item, unsave_item, get_saved_item_ids, get_user_profile, update_user_profile
from app.services.token_service import invalidate_token


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate):
    return create_user(payload)

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login_user(payload: UserLogin):
    return authenticate_user(payload)

@router.post("/admin/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def admin_login(payload: UserLogin):
    return authenticate_admin(payload)

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
    invalidate_token(token)
    return {"message": "Logged out successfully"}

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_profile(user_id: str):
    return get_user_profile(user_id)

@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_profile(user_id: str, payload: UserUpdate):
    return update_user_profile(user_id, payload)

@router.post("/{user_id}/saved-items/{product_id}")
def save_item_user(user_id: str, product_id: str):
    saved_ids = save_item(user_id, product_id)
    return {"user_id": user_id, "saved_item_ids": saved_ids}

@router.delete("/{user_id}/saved-items/{product_id}")
def unsave_item_user(user_id: str, product_id: str):
    saved_ids = unsave_item(user_id, product_id)
    return {"user_id": user_id, "saved_item_ids": saved_ids}

@router.get("/{user_id}/saved-items")
def get_saved_items_user(user_id: str):
    saved_ids = get_saved_item_ids(user_id)
    return {"user_id": user_id, "saved_item_ids": saved_ids}