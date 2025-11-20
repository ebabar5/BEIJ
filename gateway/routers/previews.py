from fastapi import APIRouter, Query
from typing import List, Dict, Any, Optional
import logging

from services.backend_client import backend_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/previews", tags=["previews"])

class PreviewResponse:
    """Transform backend preview data for frontend consumption"""
    
    @staticmethod
    def transform(backend_preview: Dict[str, Any]) -> Dict[str, Any]:
        """Transform backend preview to frontend format"""
        return {
            "id": backend_preview.get("product_id"),
            "name": backend_preview.get("product_name"),
            "price": backend_preview.get("discounted_price"),
            "rating": backend_preview.get("rating"),
            # Add additional frontend-specific fields
            "currency": "USD",  # Default currency
            "inStock": True,    # Default availability
        }
    
    @staticmethod
    def transform_list(backend_previews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform list of backend previews"""
        return [PreviewResponse.transform(preview) for preview in backend_previews]

@router.get("", response_model=List[Dict[str, Any]])
async def get_product_previews():
    """Get all product previews (frontend-optimized)"""
    try:
        logger.info("Gateway: Fetching all product previews")
        backend_response = await backend_client.get("/previews")
        
        # Transform for frontend
        frontend_previews = PreviewResponse.transform_list(backend_response)
        
        logger.info(f"Gateway: Returning {len(frontend_previews)} product previews")
        return frontend_previews
        
    except Exception as e:
        logger.error(f"Error fetching product previews: {e}")
        raise

@router.get("/filtered", response_model=List[Dict[str, Any]])
async def get_filtered_previews(
    categories: Optional[str] = Query(None, description="Categories separated by * (e.g., 'Electronics*Books')"),
    min_price: Optional[int] = Query(None, description="Minimum price filter"),
    max_price: Optional[int] = Query(None, description="Maximum price filter")
):
    """Get filtered product previews with enhanced frontend filtering"""
    try:
        logger.info(f"Gateway: Fetching filtered previews - categories: {categories}, price: {min_price}-{max_price}")
        
        # Build filter string for backend
        filter_parts = []
        
        # Add categories
        if categories:
            filter_parts.append(categories)
        else:
            filter_parts.append("all")
        
        # Add price filters
        if min_price is not None:
            filter_parts.append(f"min={min_price}")
        if max_price is not None:
            filter_parts.append(f"max={max_price}")
        
        filter_string = "&".join(filter_parts)
        
        backend_response = await backend_client.get(f"/previews/{filter_string}")
        
        # Transform for frontend
        frontend_previews = PreviewResponse.transform_list(backend_response)
        
        logger.info(f"Gateway: Returning {len(frontend_previews)} filtered previews")
        return frontend_previews
        
    except Exception as e:
        logger.error(f"Error fetching filtered previews: {e}")
        raise

# Enhanced frontend-specific preview endpoints
@router.get("/categories", response_model=List[str])
async def get_available_categories():
    """Get list of available product categories (frontend-specific)"""
    try:
        logger.info("Gateway: Fetching available categories")
        
        # Get all products to extract categories
        backend_response = await backend_client.get("/products")
        
        # Extract unique categories
        categories = set()
        for product in backend_response:
            product_categories = product.get("category", [])
            if isinstance(product_categories, list):
                categories.update(product_categories)
            elif isinstance(product_categories, str):
                categories.add(product_categories)
        
        # Remove empty categories and sort
        categories = sorted([cat for cat in categories if cat and cat.strip()])
        
        logger.info(f"Gateway: Returning {len(categories)} categories")
        return categories
        
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        raise

@router.get("/price-range", response_model=Dict[str, float])
async def get_price_range():
    """Get min/max price range for products (frontend-specific)"""
    try:
        logger.info("Gateway: Fetching price range")
        
        # Get all products to calculate price range
        backend_response = await backend_client.get("/products")
        
        if not backend_response:
            return {"min": 0.0, "max": 0.0}
        
        prices = [
            product.get("discounted_price", 0) 
            for product in backend_response 
            if product.get("discounted_price") is not None
        ]
        
        if not prices:
            return {"min": 0.0, "max": 0.0}
        
        price_range = {
            "min": min(prices),
            "max": max(prices)
        }
        
        logger.info(f"Gateway: Price range: {price_range}")
        return price_range
        
    except Exception as e:
        logger.error(f"Error fetching price range: {e}")
        raise

@router.get("/featured", response_model=List[Dict[str, Any]])
async def get_featured_products(limit: int = Query(10, description="Number of featured products")):
    """Get featured products based on rating (frontend-specific)"""
    try:
        logger.info(f"Gateway: Fetching {limit} featured products")
        
        # Get all previews
        backend_response = await backend_client.get("/previews")
        
        # Sort by rating (descending) and take top items
        sorted_products = sorted(
            backend_response, 
            key=lambda x: x.get("rating", 0), 
            reverse=True
        )
        
        featured_products = sorted_products[:limit]
        
        # Transform for frontend
        frontend_previews = PreviewResponse.transform_list(featured_products)
        
        logger.info(f"Gateway: Returning {len(frontend_previews)} featured products")
        return frontend_previews
        
    except Exception as e:
        logger.error(f"Error fetching featured products: {e}")
        raise

@router.get("/search", response_model=List[Dict[str, Any]])
async def search_previews(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, description="Maximum number of results")
):
    """Search product previews by name (frontend-specific)"""
    try:
        logger.info(f"Gateway: Searching previews for: {q}")
        
        # Get all previews
        backend_response = await backend_client.get("/previews")
        
        # Simple text search in product names
        search_results = [
            product for product in backend_response
            if q.lower() in product.get("product_name", "").lower()
        ]
        
        # Limit results
        search_results = search_results[:limit]
        
        # Transform for frontend
        frontend_previews = PreviewResponse.transform_list(search_results)
        
        logger.info(f"Gateway: Returning {len(frontend_previews)} search results")
        return frontend_previews
        
    except Exception as e:
        logger.error(f"Error searching previews: {e}")
        raise
