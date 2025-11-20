from fastapi import APIRouter, status, Header, HTTPException
from app.schemas.user import UserCreate, UserResponse, UserLogin, LoginResponse
from app.services.user_service import create_user, authenticate_user
from app.services.token_service import invalidate_token

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate):
    return create_user(payload)

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login_user(payload: UserLogin):
    return authenticate_user(payload)

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
    invalidate_token(token)
    return {"message": "Logged out successfully"}
