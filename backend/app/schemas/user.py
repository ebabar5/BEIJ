from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from typing import Optional


class User(BaseModel):
    user_id: str
    username: str
    email: EmailStr
    hashed_password: str
    is_admin: bool= False

class UserCreate(BaseModel):
    username: str = Field(...,min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(...,min_length=8)

class UserResponse(BaseModel):
    user_id: str
    username: str
    email: EmailStr
    is_admin: bool=False


class UserLogin(BaseModel):
    username_or_email: str = Field(...,min_length=3, max_length=50)
    password: str = Field(...,min_length=8)
    remember_me: bool = Field(default=False)


class LoginResponse(BaseModel):
    user: UserResponse
    token:str
    expires_in:int 

class UserUpdate(BaseModel):
    username: Optional[str]= Field(None,min_length=3, max_length=50)
    email: Optional[EmailStr] =None
    password: Optional[str] = Field(None,min_length=8)




    
