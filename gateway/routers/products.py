from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
import logging

from services.backend_client import backend_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["products"])

# Frontend-optimized product schema
class ProductResponse:
    """Transform backend product data for frontend consumption"""
    
    @staticmethod
    def transform(backend_product: Dict[str, Any]) -> Dict[str, Any]:
        """Transform backend product to frontend format"""
        return {
            "id": backend_product.get("product_id"),
            "name": backend_product.get("product_name"),
            "categories": backend_product.get("category", []),
            "price": {
                "current": backend_product.get("discounted_price"),
                "original": backend_product.get("actual_price"),
                "discount": backend_product.get("discount_percentage")
            },
            "rating": {
                "score": backend_product.get("rating"),
                "count": backend_product.get("rating_count")
            },
            "description": backend_product.get("about_product"),
            "image": backend_product.get("img_link"),
            "productUrl": backend_product.get("product_link"),
            "reviews": {
                "userIds": backend_product.get("user_id", []),
                "userNames": backend_product.get("user_name", []),
                "reviewIds": backend_product.get("review_id", []),
                "titles": backend_product.get("review_title", []),
                "content": backend_product.get("review_content")
            }
        }
    
    @staticmethod
    def transform_list(backend_products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform list of backend products"""
        return [ProductResponse.transform(product) for product in backend_products]

@router.get("", response_model=List[Dict[str, Any]])
async def get_products():
    """Get all products (frontend-optimized)"""
    try:
        logger.info("Gateway: Fetching all products")
        backend_response = await backend_client.get("/products")
        
        # Transform for frontend
        frontend_products = ProductResponse.transform_list(backend_response)
        
        logger.info(f"Gateway: Returning {len(frontend_products)} products")
        return frontend_products
        
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        raise

@router.get("/{product_id}", response_model=Dict[str, Any])
async def get_product(product_id: str):
    """Get single product by ID (frontend-optimized)"""
    try:
        logger.info(f"Gateway: Fetching product {product_id}")
        backend_response = await backend_client.get(f"/products/{product_id}")
        
        # Transform for frontend
        frontend_product = ProductResponse.transform(backend_response)
        
        logger.info(f"Gateway: Returning product {product_id}")
        return frontend_product
        
    except Exception as e:
        logger.error(f"Error fetching product {product_id}: {e}")
        raise

@router.post("", response_model=Dict[str, Any])
async def create_product(product_data: Dict[str, Any]):
    """Create new product"""
    try:
        logger.info("Gateway: Creating new product")
        
        # Transform frontend data to backend format if needed
        backend_data = {
            "product_name": product_data.get("name"),
            "category": product_data.get("categories", []),
            "discounted_price": product_data.get("price", {}).get("current"),
            "actual_price": product_data.get("price", {}).get("original"),
            "discount_percentage": product_data.get("price", {}).get("discount", "0%"),
            "rating": product_data.get("rating", {}).get("score", 0.0),
            "rating_count": product_data.get("rating", {}).get("count", 0),
            "about_product": product_data.get("description", ""),
            "user_id": [],
            "user_name": [],
            "review_id": [],
            "review_title": [],
            "review_content": "",
            "img_link": product_data.get("image", ""),
            "product_link": product_data.get("productUrl", "")
        }
        
        backend_response = await backend_client.post("/products", backend_data)
        
        # Transform response for frontend
        frontend_product = ProductResponse.transform(backend_response)
        
        logger.info("Gateway: Product created successfully")
        return frontend_product
        
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise

@router.put("/{product_id}", response_model=Dict[str, Any])
async def update_product(product_id: str, product_data: Dict[str, Any]):
    """Update existing product"""
    try:
        logger.info(f"Gateway: Updating product {product_id}")
        
        # Transform frontend data to backend format
        backend_data = {
            "product_name": product_data.get("name"),
            "category": product_data.get("categories", []),
            "discounted_price": product_data.get("price", {}).get("current"),
            "actual_price": product_data.get("price", {}).get("original"),
            "discount_percentage": product_data.get("price", {}).get("discount", "0%"),
            "rating": product_data.get("rating", {}).get("score", 0.0),
            "rating_count": product_data.get("rating", {}).get("count", 0),
            "about_product": product_data.get("description", ""),
            "user_id": product_data.get("reviews", {}).get("userIds", []),
            "user_name": product_data.get("reviews", {}).get("userNames", []),
            "review_id": product_data.get("reviews", {}).get("reviewIds", []),
            "review_title": product_data.get("reviews", {}).get("titles", []),
            "review_content": product_data.get("reviews", {}).get("content", ""),
            "img_link": product_data.get("image", ""),
            "product_link": product_data.get("productUrl", "")
        }
        
        backend_response = await backend_client.put(f"/products/{product_id}", backend_data)
        
        # Transform response for frontend
        frontend_product = ProductResponse.transform(backend_response)
        
        logger.info(f"Gateway: Product {product_id} updated successfully")
        return frontend_product
        
    except Exception as e:
        logger.error(f"Error updating product {product_id}: {e}")
        raise

@router.delete("/{product_id}")
async def delete_product(product_id: str):
    """Delete product"""
    try:
        logger.info(f"Gateway: Deleting product {product_id}")
        
        await backend_client.delete(f"/products/{product_id}")
        
        logger.info(f"Gateway: Product {product_id} deleted successfully")
        return {"message": f"Product {product_id} deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting product {product_id}: {e}")
        raise

# Additional frontend-specific endpoints
@router.get("/search", response_model=List[Dict[str, Any]])
async def search_products(
    q: Optional[str] = Query(None, description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    min_rating: Optional[float] = Query(None, description="Minimum rating")
):
    """Search and filter products (frontend-specific endpoint)"""
    try:
        logger.info(f"Gateway: Searching products with query: {q}")
        
        # Get all products from backend
        backend_response = await backend_client.get("/products")
        
        # Apply frontend-specific filtering
        filtered_products = backend_response
        
        if q:
            # Simple text search in product name and description
            filtered_products = [
                p for p in filtered_products 
                if q.lower() in p.get("product_name", "").lower() 
                or q.lower() in p.get("about_product", "").lower()
            ]
        
        if category:
            filtered_products = [
                p for p in filtered_products
                if category.lower() in [cat.lower() for cat in p.get("category", [])]
            ]
        
        if min_price is not None:
            filtered_products = [
                p for p in filtered_products
                if p.get("discounted_price", 0) >= min_price
            ]
        
        if max_price is not None:
            filtered_products = [
                p for p in filtered_products
                if p.get("discounted_price", float('inf')) <= max_price
            ]
        
        if min_rating is not None:
            filtered_products = [
                p for p in filtered_products
                if p.get("rating", 0) >= min_rating
            ]
        
        # Transform for frontend
        frontend_products = ProductResponse.transform_list(filtered_products)
        
        logger.info(f"Gateway: Returning {len(frontend_products)} filtered products")
        return frontend_products
        
    except Exception as e:
        logger.error(f"Error searching products: {e}")
        raise
