from pydantic import BaseModel
from typing import List

class ProductPreview(BaseModel):
    product_id: str
    product_name: str
    discounted_price: float
    rating: float
