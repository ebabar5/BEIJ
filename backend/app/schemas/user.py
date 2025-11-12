from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class User(BaseModel):
    user_id: str
    username: str
    email: EmailStr
    hashed_password: str

class UserCreate(BaseModel):
    username: str=Field(...,min_length=3, max_length=50)
    email: EmailStr
    password: str=Field(...,min_length=8)

class UserResponse(BaseModel):
    user_id: str
    username: str
    email: EmailStr

