from fastapi import APIRouter, status
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user

router = APIRouter(prefix="/users",tags=["users"])

@router.post("/register",response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate):
    return create_user(payload)


