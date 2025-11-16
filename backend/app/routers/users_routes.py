from fastapi import APIRouter, status
from app.schemas.user import UserCreate, UserResponse,UserLogin
from app.services.user_service import create_user,authenticate_user

router = APIRouter(prefix="/users",tags=["users"])

@router.post("/register",response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate):
    return create_user(payload)

@router.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
def login_user(payload: UserLogin):
    return authenticate_user(payload)

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout_user():
    return {"message": "Logged out succesfully"}
