from fastapi import APIRouter
from typing import List

from app.schemas.product_preview import ProductPreview
from app.services.preview_service import (
    get_all_product_previews, 
    filter_previews, 
    parse_to_previews
)
from app.services.search_service import keyword_search

# Router for product previews and search functionality
# Previews are lightweight versions of products for listing/browsing
router = APIRouter(
    prefix="/api/v1/previews",
    tags=["previews"]
)

@router.get("/", response_model=List[ProductPreview])
def get_previews():
    """Get all product previews"""
    return get_all_product_previews()

@router.get("/{fil}", response_model=List[ProductPreview])
def filter_previews_endpoint(fil: str = ""):
    """Get filtered product previews based on category or other criteria"""
    return filter_previews(fil)

# Search endpoints - note these need specific ordering
# More specific routes should come BEFORE more general ones in FastAPI

@router.get("/search/", response_model=str, tags=["search"])
def no_search_entry():
    """Search endpoint without query - returns helpful message"""
    return "Please enter a search query"

@router.get("/search/w={search_string}", response_model=List[ProductPreview], tags=["search"])
def wide_keyword_search(search_string: str):
    """
    Wide keyword search - searches across multiple product fields
    Format: /search/w=keyword1 keyword2&filter
    Can combine keywords (space-separated) with optional filter (after &)
    """
    # Split search string into keywords and optional filter
    splice = search_string.split("&", 1)
    keywords = splice[0].split(" ")
    
    if len(splice) > 1:
        # Search with filter applied
        return parse_to_previews(keyword_search(keywords, filter=splice[1]))
    else:
        # Search without filter
        return parse_to_previews(keyword_search(keywords))

@router.get("/search/{search_string}", response_model=List[ProductPreview], tags=["search"])
def strict_keyword_search(search_string: str):
    """
    Strict keyword search (default) - exact matches only
    Format: /search/keyword1 keyword2&filter
    Can combine keywords (space-separated) with optional filter (after &)
    """
    # Split search string into keywords and optional filter
    splice = search_string.split("&", 1)
    keywords = splice[0].split(" ")
    
    if len(splice) > 1:
        # Search with filter applied
        return parse_to_previews(keyword_search(keywords, filter=splice[1]))
    else:
        # Search without filter
        return parse_to_previews(keyword_search(keywords))

