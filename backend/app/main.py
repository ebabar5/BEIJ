from fastapi import FastAPI, status, Query, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from app.error_handling import register_errors

from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.schemas.user import UserCreate, UserResponse, UserLogin, LoginResponse
from app.schemas.product_preview import ProductPreview

from app.services.product_service import list_products, create_product, delete_product, update_product, get_product_by_id
from app.services.user_service import create_user, authenticate_user, save_item, unsave_item, get_saved_item_ids
from app.services.token_service import invalidate_token
from app.services.preview_service import get_all_product_previews, filter_previews, parse_to_previews
from app.services.search_service import keyword_search

app = FastAPI(
    title="BEIJ E-commerce API",
    description="Centralized API with all routes in main.py",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

register_errors(app)

@app.get("/")
def home():
    return {"status": "ok", "message": "BEIJ E-commerce API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello")
def hello():
    return {"msg": "Hello World"}

@app.get("/api/v1/products", response_model=List[Product], tags=["products"])
def get_products(
    sort_by: Optional[str] = Query(
        default=None, 
        description="Optional sort order. Supported values: name, price_asc, price_desc, rating_desc"
    )
):
    """Get all products with optional sorting"""
    return list_products(sort_by=sort_by)

@app.post("/api/v1/products", response_model=Product, status_code=201, tags=["products"])
def post_product(payload: ProductCreate):
    """Create a new product"""
    return create_product(payload)

@app.get("/api/v1/products/{product_id}", response_model=Product, tags=["products"])
def get_product(product_id: str):
    """Get a single product by ID"""
    return get_product_by_id(product_id)

@app.put("/api/v1/products/{product_id}", response_model=Product, tags=["products"])
def put_product(product_id: str, payload: ProductUpdate):
    """Update an existing product"""
    return update_product(product_id, payload)

@app.delete("/api/v1/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["products"])
def remove_product(product_id: str):
    """Delete a product"""
    delete_product(product_id)
    return None

@app.post("/api/v1/users/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["users"])
def register_user(payload: UserCreate):
    """Register a new user"""
    return create_user(payload)

@app.post("/api/v1/users/login", response_model=LoginResponse, status_code=status.HTTP_200_OK, tags=["users"])
def login_user(payload: UserLogin):
    """Login user"""
    return authenticate_user(payload)

@app.post("/api/v1/users/logout", status_code=status.HTTP_200_OK, tags=["users"])
def logout_user(authorization: str = Header(None)):
    """Logout user"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
    invalidate_token(token)
    return {"message": "Logged out successfully"}

@app.post("/api/v1/users/{user_id}/saved-items/{product_id}", tags=["users"])
def save_item_user(user_id: str, product_id: str):
    """Save an item to user's saved list"""
    saved_ids = save_item(user_id, product_id)
    return {"user_id": user_id, "saved_item_ids": saved_ids}

@app.delete("/api/v1/users/{user_id}/saved-items/{product_id}", tags=["users"])
def unsave_item_user(user_id: str, product_id: str):
    """Remove an item from user's saved list"""
    saved_ids = unsave_item(user_id, product_id)
    return {"user_id": user_id, "saved_item_ids": saved_ids}

@app.get("/api/v1/users/{user_id}/saved-items", tags=["users"])
def get_saved_items_user(user_id: str):
    """Get user's saved items"""
    saved_ids = get_saved_item_ids(user_id)
    return {"user_id": user_id, "saved_item_ids": saved_ids}

@app.get("/api/v1/previews", response_model=List[ProductPreview], tags=["previews"])
def get_previews():
    """Get all product previews"""
    return get_all_product_previews()

@app.get("/api/v1/previews/{fil}", response_model=List[ProductPreview], tags=["previews"])
def filter_previews_endpoint(fil: str = ""):
    """Get filtered product previews"""
    return filter_previews(fil)

@app.get("/api/v1/previews/search/", response_model=str, tags=["search"])
def no_search_entry():
    """Search endpoint without query"""
    return "Please enter a search query"

@app.get("/api/v1/previews/search/w={search_string}", response_model=List[ProductPreview], tags=["search"])
def wide_keyword_search(search_string: str):
    """Wide keyword search"""
    splice = search_string.split("&", 1)
    keywords = splice[0].split(" ")
    if len(splice) > 1:
        return parse_to_previews(keyword_search(keywords, filter=splice[1]))
    else:
        return parse_to_previews(keyword_search(keywords))

@app.get("/api/v1/previews/search/{search_string}", response_model=List[ProductPreview], tags=["search"])
def strict_keyword_search(search_string: str):
    """Strict keyword search (default)"""
    splice = search_string.split("&", 1)
    keywords = splice[0].split(" ")
    if len(splice) > 1:
        return parse_to_previews(keyword_search(keywords, filter=splice[1]))
    else:
        return parse_to_previews(keyword_search(keywords)) 
