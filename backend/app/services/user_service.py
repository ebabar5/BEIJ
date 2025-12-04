from app.schemas.user import User, UserCreate, UserResponse, UserLogin, LoginResponse, UserUpdate
from app.repositories.users_repo import load_all, save_all
from app.repositories.products_repo import load_all as load_products
from app.services.token_service import generate_token
from app.error_handling import NotFound, BadRequest
import uuid
import bcrypt
from fastapi import HTTPException
from typing import List, Dict, Any

# constant + helper 
BCRYPT_MAX_BYTES = 72
ADMIN_SECRET = "beij-admin-secret-2024"  # In production, use environment variable

def _bcrypt_ready(password: str) -> bytes:
    password_bytes = password.encode("utf-8")
    return (
        password_bytes[:BCRYPT_MAX_BYTES]
        if len(password_bytes) > BCRYPT_MAX_BYTES
        else password_bytes
    )

def hash_password(password: str) -> str:
    pwd = _bcrypt_ready(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd, salt)
    return hashed.decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    pwd = _bcrypt_ready(password)
    return bcrypt.checkpw(pwd, hashed_password.encode("utf-8"))

def create_user(user_create:UserCreate) -> UserResponse:
    users=load_all()
    if check_duplicate_email(users, user_create.email):
        raise HTTPException(status_code=409, detail="Email already exists.")
    if check_duplicate_username(users, user_create.username):
        raise HTTPException(status_code=409, detail="Username already exists.")
    new_id = str(uuid.uuid4())
    hashed_pwd = hash_password(user_create.password)
    new_user = User(user_id=new_id, username=user_create.username.strip(), email=user_create.email, hashed_password=hashed_pwd, is_admin=False)
    users.append(new_user.model_dump())
    save_all(users)
    return build_user_response(new_user.model_dump())

def create_admin_user(user_create: UserCreate, admin_secret: str) -> UserResponse:
    """Create a new admin user, protected by an admin secret"""
    if admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Invalid admin secret.")
    
    users = load_all()
    if check_duplicate_email(users, user_create.email):
        raise HTTPException(status_code=409, detail="Email already exists.")
    if check_duplicate_username(users, user_create.username):
        raise HTTPException(status_code=409, detail="Username already exists.")
    
    new_id = str(uuid.uuid4())
    hashed_pwd = hash_password(user_create.password)
    new_user = User(
        user_id=new_id,
        username=user_create.username.strip(),
        email=user_create.email,
        hashed_password=hashed_pwd,
        is_admin=True
    )
    users.append(new_user.model_dump())
    save_all(users)
    return build_user_response(new_user.model_dump())

def list_users() -> List[UserResponse]:
    return [UserResponse(**it) for it in load_all()]

def authenticate_user(user_login: UserLogin) -> LoginResponse:
    users = load_all()
    user = find_user_by_username_or_email(users, user_login.username_or_email)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    if not verify_password(user_login.password, user.get("hashed_password")):
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    
    is_admin = user.get("is_admin", False)
    user_response = build_user_response(user)
    token_data = generate_token(user["user_id"], user["username"], user["email"], user_login.remember_me, is_admin)
    
    return LoginResponse(
        user=user_response,
        token=token_data["token"],
        expires_in=token_data["expires_in"]
    )

def find_user(users: List[Dict[str, Any]], user_id: str) -> Dict[str, Any] | None:
    return next((u for u in users if u.get("user_id") == user_id), None)

def find_user_by_username_or_email(users: List[Dict[str, Any]], username_or_email: str) -> Dict[str, Any] | None:
    return next(
        (it for it in users 
         if it.get("username") == username_or_email or it.get("email") == username_or_email),
        None
    )

def check_duplicate_username(users: List[Dict[str, Any]], username: str, exclude_user_id: str | None = None) -> bool:
    return any(
        it.get("username") == username 
        and (exclude_user_id is None or it.get("user_id") != exclude_user_id)
        for it in users
    )

def check_duplicate_email(users: List[Dict[str, Any]], email: str, exclude_user_id: str | None = None) -> bool:
    return any(
        it.get("email") == email 
        and (exclude_user_id is None or it.get("user_id") != exclude_user_id)
        for it in users
    )

def build_user_response(user: Dict[str, Any]) -> UserResponse:
    is_admin = user.get("is_admin", False)
    return UserResponse(
        user_id=user["user_id"],
        username=user["username"],
        email=user["email"],
        is_admin=is_admin
    )

def find_product(products: List[Dict[str, Any]], product_id: str) -> Dict[str, Any] | None:
    return next(
        ( p for p in products
         if p.get("id") == product_id
         or p.get("product_id") == product_id
         or p.get("asin") == product_id), None
        )

def save_item(user_id: str, product_id: str) -> List[str]:
    users = load_all()
    user = find_user(users, user_id)
    if user is None:
        raise NotFound(f"User '{user_id}' not found.")

    products = load_products()
    product = find_product(products, product_id)
    if product is None:
        raise NotFound(f"Product '{product_id}' not found.")

    saved_ids = user.get("saved_item_ids") or []
    if product_id not in saved_ids:
        saved_ids.append(product_id)
        user["saved_item_ids"] = saved_ids
        save_all(users)
    return saved_ids

def unsave_item(user_id: str, product_id: str) -> List[str]:
    users = load_all()
    user = find_user(users, user_id)
    if user is None:
        raise NotFound(f"User '{user_id}' not found.")

    saved_ids = user.get("saved_item_ids") or []
    if product_id in saved_ids:
        saved_ids.remove(product_id)
        user["saved_item_ids"] = saved_ids
        save_all(users)
    return saved_ids

def get_saved_item_ids(user_id: str) -> List[str]:
    users = load_all()
    user = find_user(users, user_id) 
    if user is None: 
        raise NotFound(f"User '{user_id}' not found.")
    return user.get("saved_item_ids") or []

def get_user_profile(user_id: str) -> UserResponse:
    users = load_all()
    user = find_user(users, user_id)
    if user is None:
        raise NotFound(f"User '{user_id}' not found.")
    
    return build_user_response(user)

def update_user_profile(user_id: str, payload: UserUpdate) -> UserResponse:
    users = load_all()
    user = find_user(users, user_id)
    if user is None:
        raise NotFound(f"User '{user_id}' not found.")
    if payload.username is not None:
        if check_duplicate_username(users, payload.username, exclude_user_id=user_id):
            raise HTTPException(status_code=409, detail="Username already exists.")
        user["username"] = payload.username.strip()  
    if payload.email is not None:
        if check_duplicate_email(users, payload.email, exclude_user_id=user_id):
            raise HTTPException(status_code=409, detail="Email already exists.")
        user["email"] = payload.email
    if payload.password is not None:
        user["hashed_password"] = hash_password(payload.password)
    save_all(users)
    
    return build_user_response(user)

def authenticate_admin(user_login: UserLogin) -> LoginResponse:
    users = load_all()
    user = find_user_by_username_or_email(users, user_login.username_or_email)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    if not verify_password(user_login.password, user.get("hashed_password")):
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    
    is_admin = user.get("is_admin", False)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Admin access required.")
    user_response = UserResponse(
        user_id=user["user_id"],
        username=user["username"],
        email=user["email"],
        is_admin=True
    )
    token_data = generate_token(user["user_id"], user["username"], user["email"], user_login.remember_me, True)
    
    return LoginResponse(
        user=user_response,
        token=token_data["token"],
        expires_in=token_data["expires_in"]
    )
