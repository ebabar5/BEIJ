from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    product_id: str
    product_name: str
    category: List[str] = []
    discounted_price: float
    actual_price: float
    discount_percentage: str
    rating: float
    rating_count: int
    about_product: str
    user_id: List[str]
    user_name: List[str]
    review_id: List[str]
    review_title: List[str]
    review_content: str
    img_link: str
    product_link: str

class ProductCreate(BaseModel):
    product_name: str
    category: List[str] = []
    discounted_price: float
    actual_price: float
    discount_percentage: str
    rating: float
    rating_count: int
    about_product: str
    user_id: List[str] = []
    user_name: List[str] = []
    review_id: List[str] = []
    review_title: List[str] = []
    review_content: str
    img_link: str
    product_link: str

class ProductUpdate(BaseModel):
    product_name: str
    category: List[str] = []
    discounted_price: float
    actual_price: float
    discount_percentage: str
    rating: float
    rating_count: int
    about_product: str
    user_id: List[str] = []
    user_name: List[str] = []
    review_id: List[str] = []
    review_title: List[str] = []
    review_content: str
    img_link: str
    product_link: str