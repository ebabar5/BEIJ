from app.schemas.user import User, UserCreate, UserResponse
from app.repositories.users_repo import load_all, save_all
import uuid
import bcrypt
from fastapi import HTTPException
from typing import List

def hash_password(password: str) -> str:
   
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
   
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_user(user_create:UserCreate) -> UserResponse:
    users=load_all()
    if any(it.get("email")== user_create.email for it in users):
        raise HTTPException(status_code=409, detail="Email already exists")
    if any(it.get("username")== user_create.username for it in users):
        raise HTTPException(status_code=409, detail="username already exists")
    new_id = str(uuid.uuid4())
    hashed_pwd = hash_password(user_create.password)
    new_user = User(user_id=new_id, username=user_create.username.strip(), email=user_create.email, hashed_password=hashed_pwd)
    users.append(new_user.dict())
    save_all(users)
    return UserResponse(user_id=new_user.user_id, username=new_user.username, email=new_user.email)

def list_users() -> List[UserResponse]:
    return [UserResponse(**it) for it in load_all()]